from pokemoncenter import check_pokemoncenter
from bestbuy import check_bestbuy
from notifier import notify

def run_checker():
    messages = []

    pc_items = check_pokemoncenter()
    if pc_items:
        messages.append("🟢 Pokémon Center:\n" + "\n\n".join(pc_items))

    bb_items = check_bestbuy()
    if bb_items:
        messages.append("🟢 Best Buy:\n" + "\n\n".join(bb_items))

    if messages:
        notify("\n\n".join(messages))
    else:
        print("[INFO] No in-stock or preorder items found.")

