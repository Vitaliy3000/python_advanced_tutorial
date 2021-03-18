import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


class User:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


def get_users():
    """Типа обращение к бд"""
    return [User(first_name='Vitaliy', last_name='Afanasyev')]


async def users(request):
    if request.method == 'GET':
        users = get_users()
        return JSONResponse(
            [
                {'first_name': user.first_name, 'last_name': user.last_name}
                for user in users
            ]
        )


app = Starlette(debug=True, routes=[
    Route('/', users),
])


if __name__ == "__main__":
    uvicorn.run(app)
