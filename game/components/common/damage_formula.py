def get_final_damage_output(source_damage, target_defense):
    return max(0, source_damage - target_defense)
