# ╔════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦════╗
# ║  ╔═╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═╗  ║
# ╠══╣                                                                                                             ╠══╣
# ║  ║    CHRISTMAS TREE                           CREATED: 2024-10-19          https://github.com/jacobleazott    ║  ║
# ║══║                                                                                                             ║══║
# ║  ╚═╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═╝  ║
# ╚════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩════╝
# ════════════════════════════════════════════════════ DESCRIPTION ════════════════════════════════════════════════════
# This file defines what we effects we actually want to run on the Christmas Tree and for how long.
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
from Effects import LEDEffects

def main():
    led_effects = LEDEffects()
    while True:
        # led_effects.run_effect_for_x_seconds(led_effects.solid_color_rainbow, duration=5, args=(5,))
        # led_effects.run_effect_for_x_seconds(led_effects.radial_rainbow, duration=2, args=(0, 5, 1.0))
        # led_effects.run_effect_for_x_seconds(led_effects.radial_rainbow, duration=2, args=(0, -5, 1.0))
        # led_effects.run_effect_for_x_seconds(led_effects.radial_rainbow, duration=5, args=(1, 5, 1.0))
        # led_effects.run_effect_for_x_seconds(led_effects.radial_rainbow, duration=5, args=(2, 5, 0.5))
        led_effects.run_effect_for_x_seconds(led_effects.random_plane, duration=10, args=(50,))
        led_effects.run_effect_for_x_seconds(led_effects.axis_rainbow, duration=2, args=(0, -0.01, 0.5))
        led_effects.run_effect_for_x_seconds(led_effects.axis_rainbow, duration=2, args=(0, 0.01, 0.5))
        led_effects.run_effect_for_x_seconds(led_effects.axis_rainbow, duration=2, args=(1, -0.01, 0.5))
        led_effects.run_effect_for_x_seconds(led_effects.axis_rainbow, duration=2, args=(1, 0.01, 0.5))
        led_effects.run_effect_for_x_seconds(led_effects.axis_rainbow, duration=2, args=(2, -0.01, 0.5))
        led_effects.run_effect_for_x_seconds(led_effects.axis_rainbow, duration=2, args=(2, 0.01, 0.5))


if __name__ == "__main__":
    main()


# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════
