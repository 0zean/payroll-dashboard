import reflex as rx


class Spline(rx.Component):
    library = "@splinetool/react-spline"
    lib_dependencies: list[str] = ["@splinetool/runtime@1.5.5"]
    tag = "Spline"
    is_default = True
    scene: rx.Var[str]


spline = Spline.create

scene = "https://prod.spline.design/1eapv4LnOygEqB66/scene.splinecode"


def spline_demo():
    return spline(scene=scene)
