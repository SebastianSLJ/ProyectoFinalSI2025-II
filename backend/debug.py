# Debug: ver qué hay en datetime
import datetime
print(f"¿Qué hay en datetime? {dir(datetime)}")
print(f"Tipo de datetime: {type(datetime)}")

# Si datetime no tiene 'now', hay un conflicto
if hasattr(datetime, 'now'):
    print("✅ datetime tiene 'now'")
else:
    print("❌ datetime NO tiene 'now' - hay conflicto de nombres")

