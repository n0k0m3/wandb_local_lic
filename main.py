from jwcrypto import jwk, jwt
from uuid import uuid4
import datetime
import json
import os

if not os.path.exists("private.json") and not os.path.exists("public.json"):
    import keygen

    keygen.generate_key()


def encode_jwt(payload):
    with open("private.json", "r") as f:
        key = jwk.JWK.from_json(f.read())
    jwt_token = jwt.JWT(
        header={"alg": "RS256", "kid": key.export_public(as_dict=True)["kid"]},
        claims=payload,
    )
    jwt_token.make_signed_token(key)
    print(jwt_token.serialize())


def main():

    # Default values
    seats = 100
    teams = 10
    expire_date = "12/31/2099"
    registeredModels = 5
    storageGigs = 1000
    concurrentAgents = 10

    # Main settings
    if input("Do you want to change the default values? (y/N): ").lower() or "n" == "y":
        seats = int(input("Enter the number of seats (100): ") or 100)
        teams = int(input("Enter the number of teams (10): ") or 10)
        expire_date = (
            input("Enter the expire date (MM/DD/YYYY) (12/31/2099): ") or "12/31/2099"
        )
        print()

        # Advanced settings
        if input("Do you want to use advanced settings? (y/N): ").lower() or "n" == "y":
            registeredModels = int(
                input("Enter the number of registered model (5): ") or 5
            )
            storageGigs = int(input("Enter the max storage size (1000): ") or 1000)
            concurrentAgents = int(
                input("Enter the max concurrent agents (10): ") or 10
            )

    timedelta = datetime.timedelta(hours=6, minutes=59, seconds=59)
    expire_time = datetime.datetime.strptime(expire_date, "%m/%d/%Y") + timedelta
    expiresAt = expire_time.replace(tzinfo=None).isoformat() + ".999Z"
    epoch = int(expire_time.strftime("%s"))

    PAYLOAD = {
        "concurrentAgents": concurrentAgents,
        "deploymentId": str(uuid4()),
        "maxTeams": teams,
        "maxRegisteredModels": registeredModels,
        "maxUsers": seats,
        "maxStorageGb": storageGigs,
        "trial": False,
        "expiresAt": expiresAt,
        "flags": [
            "SCALABLE",
            "mysql",
            "s3",
            "redis",
            "NOTIFICATIONS",
            "slack",
            "notifications",
            "MANAGEMENT",
            "org_dash",
            "auth0",
            "BYOB",
            "byob",
        ],
        "accessKey": str(uuid4()),
        "seats": seats,
        "teams": teams,
        "registeredModels": registeredModels,
        "storageGigs": storageGigs,
        "exp": epoch,
    }

    encode_jwt(PAYLOAD)


if __name__ == "__main__":
    main()
