from jwcrypto import jwk
import json

KID = "u3hx2B42AhDQs53LPcOr6vai7hJWnbqum4YNVVwUpIc="


def generate_key():
    # Generate a new key
    key = jwk.JWK.generate(kty="RSA", size=2048, use="sig", kid=KID, alg="RS256")
    pub = key.export_public(as_dict=True)
    priv = key.export_private(as_dict=True)
    pub_order = ["use", "kty", "kid", "alg", "n", "e"]
    pub = {
        k: v for k, v in sorted(pub.items(), key=lambda pair: pub_order.index(pair[0]))
    }
    with open("public.json", "w") as f:
        json.dump(pub, f, indent=4)
    with open("private.json", "w") as f:
        json.dump(priv, f, indent=4)

    jwks = {"keys": [pub]}
    with open("jwks.json", "w") as f:
        json.dump(jwks, f, indent=4)


if __name__ == "__main__":
    generate_key()
