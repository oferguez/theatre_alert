# Load environment variables
export echo $(grep -Ev '^[[:space:]]*(#|$)' .env.local | xargs)
python3 culture_officer.py
