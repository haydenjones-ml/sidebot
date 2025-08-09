from tinydb import TinyDB, Query
from datetime import datetime
from pathlib import Path
import traceback

# Ensure data directory exists
db_path = Path("ledger_db.json")
db_path.parent.mkdir(parents=True, exist_ok=True)

try:
    database = TinyDB(db_path)
    ledger = database.table("bets")
except Exception as e:
    print(f"❌ Failed to open TinyDB: {e}")
    traceback.print_exc()
    raise

def gen_bet_id() -> int:
    """Generate a new unique bet ID."""
    try:
        if len(ledger) == 0:
            return 1
        existing_ids = [bet["bet_id"] for bet in ledger.all() if "bet_id" in bet]
        return max(existing_ids) + 1
    except Exception as e:
        print(f"❌ gen_bet_id error: {e}")
        traceback.print_exc()
        raise

def add_sidebet(server_id: int, bettor1: int, bettor2: int, amount: int):
    """Insert a new bet into the ledger."""
    try:
        bet_id = gen_bet_id()
        ledger.insert({
            "bet_id": bet_id,
            "server_id": server_id,
            "bettor_1_id": bettor1,
            "bettor_2_id": bettor2,
            "amount": amount,
            "Open": True,
            "winner": None,
            "timestamp": datetime.utcnow().isoformat()
        })
        print(f"✅ Added bet {bet_id} to ledger: {bettor1} vs {bettor2} for ${amount}")
        return bet_id
    except Exception as e:
        print(f"❌ add_sidebet error: {e}")
        traceback.print_exc()
        raise

def settle(bet_id: int, winner: int):
    """Mark a bet as settled."""
    try:
        Bet = Query()
        ledger.update({
            "Open": False,
            "winner": winner
        }, Bet.bet_id == bet_id)
        print(f"✅ Settled bet {bet_id} with winner {winner}")
    except Exception as e:
        print(f"❌ settle error: {e}")
        traceback.print_exc()
        raise

def get_open_bets(server_id: int):
    """Return all open bets for a server."""
    Bet = Query()
    return ledger.search((Bet.Open == True) & (Bet.server_id == server_id))

def get_all_bets(server_id: int):
    """Return all bets for a server."""
    Bet = Query()
    return ledger.search(Bet.server_id == server_id)

def get_user_stats(user_id):
    """Calculate user betting statistics."""
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