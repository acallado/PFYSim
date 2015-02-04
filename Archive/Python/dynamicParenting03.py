import bpy

spreader_obj = bpy.ops.mesh.primitive_cube_add()


def animateContainers(spreader_obj, container_list):
    print('In animateContainers()')
    global spreader_obj
# Get reference to animated spreader obj
# For each cnt:
    # Get cnt ID
    # Get cnt animation range (ini_anim_time_range to end_anim_time_range)
    # Add 'Child Of' constraint to cnt at ini_anim_time_range
    # Set constraint target to spreader obj
    # Set Inverse correction
    # Animate constraint influence between ini_anim_time_range and the previous
    #    frame
    # Bake Action from 0 to end_anim_time_range


def main():
    print('In main()')

if __name__ == '__main__':
    main()
