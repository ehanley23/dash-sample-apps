from pybkb.common.bayesianKnowledgeBase import bayesianKnowledgeBase as BKB
from pybkb.common.bayesianKnowledgeBase import BKB_S_node

bkb = BKB()

# comp_A = bkb.addComponent('A')
# comp_B = bkb.addComponent('B')
# 
# state_a1 = bkb.addComponentState(comp_A, 'a1')
# state_a2 = bkb.addComponentState(comp_A, 'a2')
# state_b1 = bkb.addComponentState(comp_B, 'b1')
# state_b2 = bkb.addComponentState(comp_B, 'b2')
# 
# snode_1 = BKB_S_node(comp_B, state_b1, 0.45, [(comp_A, state_a1)])
# snode_2 = BKB_S_node(comp_B, state_b2, 0.55, [(comp_A, state_a1)])
# snode_3 = BKB_S_node(comp_B, state_b2, 0.2, [(comp_A, state_a2)])
# snode_4 = BKB_S_node(comp_A, state_a1, 0.1)
# snode_5 = BKB_S_node(comp_A, state_a2, 0.9)
# 
#for _snode in [snode_1, snode_2, snode_3, snode_4, snode_5]:
#    bkb.addSNode(_snode)


bkb.load('Users/Eamon/source/PyBKB/examples/IllegalDumpingEv.bkb')
bkb.save('Users/Eamon/source/PyBKB/examples/IllegalDumpingEv_binary.bkb', use_pickle=True)
_ = bkb.makeGraph() 

    
