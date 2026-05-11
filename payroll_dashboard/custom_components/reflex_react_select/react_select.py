"""Reflex custom component ReactSelect."""

# For wrapping react guide, visit https://reflex.dev/docs/wrapping-react/overview/

from typing import Any

import reflex as rx
from reflex.components.component import NoSSRComponent

# Some libraries you want to wrap may require dynamic imports.
# This is because they they may not be compatible with Server-Side Rendering (SSR).
# To handle this in Reflex, all you need to do is subclass `NoSSRComponent` instead.
# For example:
# from reflex.components.component import NoSSRComponent
# class ReactSelect(NoSSRComponent):
#     pass


class ReactSelect(NoSSRComponent):
    """ReactSelect component."""

    # The React library to wrap.
    library = "react-select"

    # The React component tag.
    tag = "Select"

    # If the tag is the default export from the module, you must set is_default = True.
    # This is normally used when components don't have curly braces around them when importing.
    is_default = True

    # If you are wrapping another components with the same tag as a component in your project
    # you can use aliases to differentiate between them and avoid naming conflicts.
    # alias = "OtherReactSelect"

    # The props of the React component.
    # Note: when Reflex compiles the component to Javascript,
    # `snake_case` property names are automatically formatted as `camelCase`.
    # The prop names may be defined in `camelCase` as well.
    # some_prop: rx.Var[str] = "some default value"
    # some_other_prop: rx.Var[int] = 1

    # By default Reflex will install the library you have specified in the library property.
    # However, sometimes you may need to install other libraries to use a component.
    # In this case you can use the lib_dependencies property to specify other libraries to install.
    # lib_dependencies: list[str] = []

    # Event triggers declaration if any.
    # Below is equivalent to merging `{ "on_change": lambda e: [e] }`
    # onto the default event triggers of parent/base Component.
    # The function defined for the `on_change` trigger maps event for the javascript
    # trigger to what will be passed to the backend event handler function.
    # on_change: rx.EventHandler[lambda e: [e]]

    # To add custom code to your component
    # def _get_custom_code(self) -> str:
    #     return "const customCode = 'customCode';"

    class_name_prefix: rx.Var[str] = "react-select"

    name: rx.Var[str]
    input_id: rx.Var[str]

    options: rx.Var[list[dict[str, str]]]
    value: rx.Var[str]

    content_editable: rx.Var[bool] = True
    is_searchable: rx.Var[bool] = True
    is_clearable: rx.Var[bool] = True
    is_multi: rx.Var[bool] = False

    default_value: rx.Var[dict[str, str] | None] = None
    default_input_value: rx.Var[str | None] = None
    placeholder: rx.Var[str] = ""
    no_options_message: rx.vars.FunctionVar[Any] | None = None

    menu_is_open: rx.Var[bool | None] = None
    default_menu_is_open: rx.Var[bool] = False
    close_menu_on_select: rx.Var[bool] = True
    max_menu_height: rx.Var[int | None] = None

    on_input_change: rx.EventHandler[lambda entered_text: [entered_text]]
    on_change: rx.EventHandler[lambda option: [option]]

    # Container of the control itself (but not the menu below)
    control_style: rx.Var[rx.Style | dict | None] = rx.Style(
        {
            "background-color": rx.color("gray", 1),
            "color": rx.color("gray", 12),
            "border-color": rx.color("gray", 3),
            "border-width": "2px",
        }
    )

    # Container of the control itself when it has focus
    control_focused_style: rx.Var[rx.Style | dict | None] = rx.Style(
        {
            "border-color": rx.color("accent", 2),
        }
    )

    # This is the container that accepts input when the user types
    # Do not set the background color or it will obscure the selected value
    input_container_style: rx.Var[rx.Style | dict | None] = rx.Style(
        {
            "color": rx.color("gray", 12),
        }
    )

    # This is the container that displays the selected value (it's
    # different than the one that accepts user input).
    single_value_style: rx.Var[rx.Style | dict | None] = rx.Style(
        {
            "color": rx.color("gray", 12),
        }
    )

    # This is the container that displays a selected value of multiple
    # The color is only applied to the x for close icon
    multi_value_style: rx.Var[rx.Style | dict | None] = rx.Style(
        {
            "color": rx.color("orange", 8),
            "background-color": rx.color("gray", 3),
            "border-radius": "5px",
        }
    )

    # This styles the text in the multiple selections
    multi_value_label_style: rx.Var[rx.Style | dict | None] = rx.Style(
        {
            "color": rx.color("gray", 12),
        }
    )

    # This is the container for the overall drop down menu
    menu_style: rx.Var[rx.Style | dict | None] = rx.Style(
        {
            "background-color": rx.color("gray", 1),
            "color": rx.color("gray", 12),
            "padding": "0.4em 0.5em",
            "border-color": rx.color("gray", 3),
            "border-width": "1px",
            "border-radius": "8px",
        }
    )

    option_selected_style: rx.Var[rx.Style | dict | None] = rx.Style(
        {
            "background-color": rx.color("gray", 1),
            "color": rx.color("gray", 12),
            "font-style": "italic",
            "font-weight": "bold",
            "border-radius": "4px",
        }
    )
    option_focused_style: rx.Var[rx.Style | dict | None] = rx.Style(
        {
            "background-color": rx.color("accent", 9),
            "color": rx.color("accent", 1),
            "border-radius": "4px",
        }
    )

    def add_style(self):
        return rx.Style(
            {
                f".{self.class_name_prefix}__control": self.control_style,
                f".{self.class_name_prefix}__control--is-focused": self.control_focused_style,
                f".{self.class_name_prefix}__input-container": self.input_container_style,
                f".{self.class_name_prefix}__single-value": self.single_value_style,
                f".{self.class_name_prefix}__multi-value": self.multi_value_style,
                f".{self.class_name_prefix}__multi-value__label": self.multi_value_label_style,
                f".{self.class_name_prefix}__menu": self.menu_style,
                f".{self.class_name_prefix}__option--is-selected": self.option_selected_style,
                f".{self.class_name_prefix}__option--is-focused": self.option_focused_style,
            }
        )


react_select = ReactSelect.create
