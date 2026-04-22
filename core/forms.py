class BootstrapFormMixin:
    # This mixin injects unified css classes into form fields.
    def _apply_bootstrap_classes(self):
        for field_name, field in self.fields.items():
            widget = field.widget
            css_class = widget.attrs.get("class", "")
            if widget.__class__.__name__ in {"CheckboxInput"}:
                widget.attrs["class"] = f"{css_class} form-check-input".strip()
            else:
                base_class = "form-select" if widget.__class__.__name__ in {"Select", "SelectMultiple"} else "form-control"
                widget.attrs["class"] = f"{css_class} {base_class}".strip()
            if not widget.attrs.get("placeholder") and field.label:
                widget.attrs["placeholder"] = str(field.label)
