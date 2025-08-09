from tinydb import TinyDB, Query
from datetime import datetime

database = TinyDB("ledger_db.json")
ledger = database.table("bets")

def gen_bet_id() -> int:
    return len(ledger) + 1

def add_sidebet(server_id: int, bettor1: int, bettor2: int, amount: int):
    bet_id = gen_bet_id()
    ledger.insert({
        "bet_id": bet_id,
        "server_id": server_id,
        "bettor_1_id": bettor1,
        "bettor_2_id": bettor2,  # Fixed key typo here
        "amount": amount,
        "Open": True,
        "winner": None,
        "timestamp": datetime.utcnow().isoformat()
    })
    return bet_id

def settle(bet_id: int, winner: int):
    Bet = Query()
    ledger.update({
        "Open": False,
        "winner": winner
    }, Bet.bet_id == bet_id)

def get_open_bets(server_id: int):
    Bet = Query()
    return ledger.search((Bet.Open == True) & (Bet.server_id == server_id))

def get_all_bets(server_id: int):
    Bet = Query()
    return ledger.search(Bet.server_id == server_id)

def get_user_stats(user_id):
    total = wins = amount_won = amount_lost = 0
    for bet in ledger.all():
        involved = user_id in [bet["bettor_1_id"], bet["bettor_2_id"]]
        if not involved or bet.get("Open", True):  # Only count settled bets
            continue
        total += 1
        if bet["winner"] == user_id:
            wins += 1
            amount_won += bet["amount"]
        else:
            amount_lost += bet["amount"]
    return {
        "total_bets": total,
        "wins": wins,
        "win_rate": round((wins / total) * 100, 2) if total else 0,
        "amount_won": amount_won,
        "amount_lost": amount_lost,
        "net_gain": amount_won - amount_lost
    }