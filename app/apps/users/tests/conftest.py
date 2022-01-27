from io import BytesIO

# user example
# I use it as users request.data
from apps.users.constants import PHOTO_BYTE

USER = [{
    "gender": "male",
    "first_name": "Mateusz",
    "last_name": "Perkins",
    "country": "United Kingdom",
    "city": "Opole",
    "email": "mario.perkins@example.com",
    "username": "organicgoose823",
    "phone": "0716-846-384"
}]


# faking data from random user api
# used in first requests.get
def mock_api_data(n):
    results = []
    for i in range(n):
        results.append({
            "gender": f"female",
            "name": {
                "first": f"Test{i}",
                "last": f"Testing{i}"
            },
            "location": {
                "country": f"Testoland{i}",
                "city": f"Tes{i}"
            },
            "email": f"test.test{i}@example.com",
            "login": {
                "username": f"test_username{i}"
            },
            "cell": f"14567{i}{i}63",
            "picture": {
                'large': 'https://randomuser.me/api/portraits/women/37.jpg'
            }
        })
    return results


# list of bytesIO objects to fake
def _get_photo_bytes(n_photos):
    return [BytesIO(PHOTO_BYTE) for _ in range(n_photos)]
