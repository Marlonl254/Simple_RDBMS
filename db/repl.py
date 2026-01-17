from db.engine import db

print("Simple RDBMS REPL. Type 'exit' to quit.")
while True:
    cmd = input("SQL> ").strip()
    if cmd.lower() in ("exit", "quit"):
        break
    try:
        res = db.execute(cmd)
        print(res)
    except Exception as e:
        print("Error:", e)
