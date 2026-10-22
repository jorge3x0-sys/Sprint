import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/pau/Universidad/script2/install/g10_prii3_move_turtlebot'
