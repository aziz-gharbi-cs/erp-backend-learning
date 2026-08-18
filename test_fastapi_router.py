from fastapi import APIRouter, FastAPI


app = FastAPI()

router = APIRouter(
    prefix="/redis",
    tags=["Redis"],
)


@router.get("/test")
def test():
    return {"message": "works"}


print("Before:")
print([route.path for route in app.routes if hasattr(route, "path")])

app.include_router(router)

print("After:")
print([route.path for route in app.routes if hasattr(route, "path")])