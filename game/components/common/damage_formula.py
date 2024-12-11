def get_final_damage_output(source_power, target_defense):
    return max(0, source_power - target_defense)
