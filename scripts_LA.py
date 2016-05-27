__author__ = "Jerome Thai, Nicolas Laurent-Brouty"
__email__ = "jerome.thai@berkeley.edu, nicolas.lb@berkeley.edu"

'''
Scripts for LA network
'''

import numpy as np
from process_data import process_net, process_net_attack, process_trips, extract_features, process_links, \
    geojson_link, construct_igraph, construct_od, join_node_demand
from frank_wolfe_2 import solver, solver_2, solver_3, single_class_parametric_study

from multi_types_solver import parametric_study
from frank_wolfe_heterogeneous import parametric_study_2

from metrics import average_cost_all_or_nothing, all_or_nothing_assignment, \
    cost_ratio, cost, save_metrics, path_cost
from utils import multiply_cognitive_cost, heterogeneous_demand, \
    net_with_marginal_cost
from metrics import OD_routed_costs, OD_non_routed_costs, free_flow_OD_costs
from AoN_igraph import all_or_nothing


def process_LA_node():
    lines = open("data/LA_node.txt", "r").readlines()
    code = 'data=' + lines[0]
    exec code
    array = np.zeros((len(data), 3))
    for node in data:
        array[int(node[1]['nid'])-1, 0] = node[1]['nid']
        array[int(node[1]['nid'])-1, 1] = node[1]['coords'][1]
        array[int(node[1]['nid'])-1, 2] = node[1]['coords'][0]
    np.savetxt('data/LA_node.csv', array, delimiter=',')


def process_LA_net():
    process_net('data/LA_net.txt', 'data/LA_net.csv')

def process_LA_net_attack(thres,beta):
    process_net_attack('data/LA_net.txt', 'data/LA_net_attack.csv',thres,beta)

def process_LA_od():
    process_trips('data/LA_od.txt', 'data/LA_od.csv')


def remove_loops_in_LA_od():
    out = ['O,D,demand\n']
    demand = np.loadtxt('data/LA_od.csv', delimiter=',', skiprows=1)
    for row in range(demand.shape[0]):
        o = int(demand[row,0])
        d = int(demand[row,1])
        if o != d:
            out.append('{},{},{}\n'.format(o,d,demand[row,2]))
    with open('data/LA_od.csv', 'w') as f:
        f.write(''.join(out))


def remove_doublons_in_LA_od():
    demand = np.loadtxt('data/LA_od_2.csv', delimiter=',', skiprows=1)
    out = [demand[0,:]]
    for i in range(1,demand.shape[0]):
        if demand[i,1] == demand[i-1,1]:
            out[-1][2] = out[-1][2] + demand[i,2]
        else:
            out.append(demand[i,:])
    np.savetxt('data/LA_od_3.csv', np.array(out), delimiter=',', \
        header='O,D,flow', comments='')


def load_LA():
    graph = np.loadtxt('data/LA_net.csv', delimiter=',', skiprows=1)
    demand = np.loadtxt('data/LA_od.csv', delimiter=',', skiprows=1)
    node = np.loadtxt('data/LA_node.csv', delimiter=',')
    return graph, demand, node


def load_LA_2():
    graph = np.loadtxt('data/LA_net.csv', delimiter=',', skiprows=1)
    demand = np.loadtxt('data/LA_od_2.csv', delimiter=',', skiprows=1)
    node = np.loadtxt('data/LA_node.csv', delimiter=',')
    # features = table in the format [[capacity, length, FreeFlowTime]]
    features = extract_features('data/LA_net.txt')
    # increase capacities of these two links because they have a travel time
    # in equilibrium that that is too big
    features[10787,0] = features[10787,0] * 1.5
    graph[10787,-1] = graph[10787,-1] / (1.5**4)
    features[3348,:] = features[3348,:] * 1.2
    graph[3348,-1] = graph[3348,-1] / (1.2**4)
    return graph, demand, node, features


def load_LA_3():
    graph = np.loadtxt('data/LA_net.csv', delimiter=',', skiprows=1)
    demand = np.loadtxt('data/LA_od_3.csv', delimiter=',', skiprows=1)
    node = np.loadtxt('data/LA_node.csv', delimiter=',')
    # features = table in the format [[capacity, length, FreeFlowTime]]
    features = extract_features('data/LA_net.txt')
    # increase capacities of these two links because they have a travel time
    # in equilibrium that that is too big
    features[10787,0] = features[10787,0] * 1.5
    graph[10787,-1] = graph[10787,-1] / (1.5**4)
    features[3348,:] = features[3348,:] * 1.2
    graph[3348,-1] = graph[3348,-1] / (1.2**4)
    # divide demand going to node 106 by 10 because too large
    for i in range(demand.shape[0]):
        if demand[i,1] == 106.:
            demand[i,2] = demand[i,2] / 10.
    return graph, demand, node, features

def load_LA_4():
    graph = np.loadtxt('data/LA_net_attack.csv', delimiter=',', skiprows=1)
    demand = np.loadtxt('data/LA_od_3.csv', delimiter=',', skiprows=1)
    node = np.loadtxt('data/LA_node.csv', delimiter=',')
    # features = table in the format [[capacity, length, FreeFlowTime]]
    features = extract_features('data/LA_net.txt')
    # increase capacities of these two links because they have a travel time
    # in equilibrium that that is too big
    features[10787,0] = features[10787,0] * 1.5
    graph[10787,-1] = graph[10787,-1] / (1.5**4)
    features[3348,:] = features[3348,:] * 1.2
    graph[3348,-1] = graph[3348,-1] / (1.2**4)
    # divide demand going to node 106 by 10 because too large
    for i in range(demand.shape[0]):
        if demand[i,1] == 106.:
            demand[i,2] = demand[i,2] / 10.
    return graph, demand, node, features

def check__LA_connectivity():
    graph, demand, node = load_LA()
    print np.min(graph[:,1:3])
    print np.max(graph[:,1:3])
    print np.min(demand[:,:2])
    print np.max(demand[:,:2])
    od = construct_od(demand)
    g = construct_igraph(graph)
    f = np.zeros((graph.shape[0],))
    print average_cost_all_or_nothing(f, graph, demand)


def frank_wolfe_on_LA():
    graph, demand, node, features = load_LA_2()
    demand[:,2] = demand[:,2] / 4000.
    f = solver_3(graph, demand, max_iter=1000, q=50, display=1, stop=1e-2)
    np.savetxt('data/LA/LA_output_4.csv', f, delimiter=',')


def visualize_LA_capacity():
    graph, demand, node = load_LA()
    features = extract_features('data/LA_net.txt')
    links = process_links(graph, node, features, in_order=True)
    color = features[:,0] # we choose to color by the capacities
    names = ['capacity', 'length', 'fftt']
    # color = 2.1 * features[:,0] / 2000.
    color = 2.*(features[:,0] <= 900.) + 5.*(features[:,0] > 900.)
    weight = (features[:,0] <= 900.) + 3.*(features[:,0] > 900.)
    geojson_link(links, names, color, weight)


def visualize_LA_demand():
    net, demand, node, features = load_LA_2()
    ods = join_node_demand(node, demand)
    B = np.random.randint(ods.shape[0], size=100)
    ods = ods[B,:]
    color = ods[:,4] / 10. # for demand
    geojson_link(ods, ['demand'], color)


def visualize_LA_total_flows(alpha, only_local=False):
    '''
    visualize total flow in L.A. using total_link_flows.csv as input
    '''
    net, demand, node, geom = load_LA_2()
    f = np.loadtxt('data/LA/total_link_flows.csv', delimiter=',', \
        skiprows=1)
    names = ['link_id', 'capacity', 'length', 'fftt', 'local', 'flow']
    features = np.zeros((f.shape[0], 6))
    features[:,0] = net[:,0]
    features[:,1:4] = geom
    features[:,4] = f[:,6]
    features[:,5] = f[:,7+int(alpha/10.)]
    links = process_links(net, node, features, in_order=True)
    color = features[:,5] * 10.
    color = color + (color > 0.0)
    weight = (features[:,1] <= 900.) + 2.*(features[:,1] > 900.)
    if only_local:
        links = links[weight==1.0, :]
        color = color[weight==1.0]
        weight = weight[weight==1.0]
    geojson_link(links, names, color, weight)


def visualize_LA_flow_variation(only_local=False):
    '''
    visualize the variations in link flows
    '''
    net, demand, node, geom = load_LA_2()
    data = np.loadtxt("data/LA/link_variation.csv", delimiter=',', skiprows=1)
    links = process_links(data[:,:3], node, data[:,[0,3,4,5,6,19,20,21]], \
        in_order=True)
    names = ['link_id','capacity','length','fftt','local','max_id','inc','dec']
    color = (data[:,19] - 1.) / 2.
    weight = (data[:,6] == 1.) + 3.*(data[:,6] == 0.)
    if only_local:
        links = links[weight==1.0, :]
        color = color[weight==1.0]
        weight = weight[weight==1.0]
    geojson_link(links, names, color, weight)



def visualize_LA_result():
    net, demand, node = load_LA()
    f = np.loadtxt('data/LA_output.csv', delimiter=',', skiprows=0)
    features = np.zeros((f.shape[0], 4))
    features[:,:3] = extract_features('data/LA_net.txt')
    f = np.divide(f, features[:,0])
    features[:,3] = f
    links = process_links(net, node, features, in_order=True)
    color = 2.0*f + 1.0
    geojson_link(links, ['capacity', 'length', 'fftt', 'flow_over_capacity'], color)


def check_LA_result():
    net, demand, node, features = load_LA_2()
    demand[:,2] = demand[:,2] / 4000.
    f = np.loadtxt('data/LA/LA_output_4.csv', delimiter=',', skiprows=0)
    costs = cost(f, net)
    cr = cost_ratio(f, net)
    print np.sort(cr)[-20:]
    for row in range(net.shape[0]):
        if cr[row] >= 10.: 
            print cr[row]
            print net[row,:3], features[row,:]
    L = all_or_nothing_assignment(costs, net, demand)
    print costs.dot(L) / np.sum(demand[:,2])


def reduce_demand():
    net, demand, node = load_LA()
    features = extract_features('data/LA_net.txt')
    f = np.loadtxt('data/LA/LA_output_3.csv', delimiter=',', skiprows=0)
    cr = cost_ratio(f, net)
    for row in range(net.shape[0]):
        if cr[row] >= 10.: 
            out = []
            for i in range(demand.shape[0]):
                if int(demand[i,0]) == int(net[row,1]):
                    out.append(demand[i,2])
                    demand[i,2] = demand[i,2] / 10.
            if len(out) > 0:
                out = np.array(out)
                print '\nratio:', cr[row]
                print 'origin: {}\nflow: {}'.format(int(demand[i,0]), np.sum(out))
                print np.sort(out).tolist()

    for row in range(net.shape[0]):
        if cr[row] >= 10.: 
            out = []
            for i in range(demand.shape[0]):
                if int(demand[i,1]) == int(net[row,2]):
                    out.append(demand[i,2])
                    demand[i,2] = demand[i,2] / 10.

            if len(out) > 0:
                out = np.array(out)
                print '\nratio:', cr[row]
                print 'destination: {}\nflow: {}'.format(int(demand[i,0]), np.sum(out))
                print np.sort(out).tolist()

    # np.savetxt('data/LA_od_2.csv', demand, delimiter=',', header='O,D,flow')


def increase_capacity():
    net, demand, node = load_LA()
    f = np.loadtxt('data/LA/LA_output_3.csv', delimiter=',', skiprows=0)
    cr = cost_ratio(f, net)


def LA_parametric_study(alphas):
    g, d, node, feat = load_LA_2()
    d[:,2] = d[:,2] / 4000.
    parametric_study(alphas, g, d, node, feat, 1000., 3000., 'data/LA/test_{}.csv',\
        stop=1e-3, stop_cycle=1e-3)


def LA_parametric_study_2(alphas):
    g, d, node, feat = load_LA_2()
    d[:,2] = d[:,2] / 4000.
    parametric_study_2(alphas, g, d, node, feat, 1000., 3000., 'data/LA/test_{}.csv',\
        stop=1e-3)


def LA_metrics(alphas, input, output):
    net, d, node, features = load_LA_3()
    # import pdb; pdb.set_trace()
    d[:,2] = d[:,2] / 4000.
    net2, small_capacity = multiply_cognitive_cost(net, features, 1000., 3000.)
    save_metrics(alphas, net, net2, d, features, small_capacity, input, \
        output, skiprows=1, \
        length_unit='Meter', time_unit='Second')

def LA_parametric_study_attack(alphas,thres,beta):
    process_LA_net_attack(thres,beta)
    g, d, node, feat = load_LA_4()
    d[:,2] = d[:,2] / 4000.
    parametric_study_2(alphas, g, d, node, feat, 1000., 3000., 'data/LA/test_attack_{}.csv',\
        stop=1e-3)

#beta is the coefficient of reduction of capacity: capacity = beta*capacity
#load_LA_4() loads the modified network
def LA_metrics_attack(alphas, input, output, beta):
    net, d, node, features = load_LA_4()
    # import pdb; pdb.set_trace()
    d[:,2] = d[:,2] / 4000.
    net2, small_capacity = multiply_cognitive_cost_attack(net, features,beta, 1000., 3000.)
    save_metrics(alphas, net, net2, d, features, small_capacity, input, \
        output, skiprows=1, \
        length_unit='Meter', time_unit='Second')


def LA_routed_costs(alphas, input, output):
    net, demand, node, features = load_LA_3()
    OD_routed_costs(alphas, net, demand, input, output, verbose=1)


def LA_non_routed_costs(alphas, input, output):
    net, demand, node, features = load_LA_3()
    net2, small_capacity = multiply_cognitive_cost(net, features, 1000., 3000.)
    OD_non_routed_costs(alphas, net, net2, demand, input, output, verbose=1)


def total_link_flows(alphas, input, output):
    '''
    output numpy array with total link flows (non-routed + routed) of the form:
    link_id,from,to,capacity,length,fftt,local,X0,...,X100
    '''
    net, demand, node, features = load_LA_2()
    net2, small_capacity = multiply_cognitive_cost(net, features, 1000., 3000.)
    links = net.shape[0]
    n_alpha = len(alphas)
    out = np.zeros((links, 7+n_alpha))
    out[:,:3] = net[:,:3]
    out[:,3:6] = features
    out[:,6] = small_capacity
    col_alphas = ','.join(['X'+str(int(alpha*100)) for alpha in alphas])
    columns = 'link_id,from,to,capacity,length,fftt,local,' + col_alphas
    for i,alpha in enumerate(alphas):
        fs = np.loadtxt(input.format(int(alpha*100)), delimiter=',', skiprows=1)
        out[:,i+7] = np.sum(fs,1)
    np.savetxt(output, out, delimiter=',', header=columns, comments='')


def LA_free_flow_costs(thres, cog_costs):
    '''
    study aiming at comparing the OD costs of all-or-nothing assignment
    between costs = travel times, and costs with multiplicative cognitive costs
    '''
    net, demand, node, geom = load_LA_2()
    g = construct_igraph(net)
    g2 = construct_igraph(net)
    od = construct_od(demand)
    print np.array(g.es["weight"]).dot(all_or_nothing(g, od))/ (np.sum(demand[:,2])*60.)
    for K in cog_costs:
        net2, small_capacity = multiply_cognitive_cost(net, geom, thres, K)
        g2.es["weight"] = net2[:,3]
        print np.array(g.es["weight"]).dot(all_or_nothing(g2, od))/ (np.sum(demand[:,2])*60.)


def LA_OD_free_flow_costs(thres, cog_costs, output, verbose=0):
    '''
    computes OD costs (free-flow travel times) for non-routed users
    under different levels of cognitive costs for links with capacity under thres
    '''
    net, demand, node, geom = load_LA_3()
    costs = []
    for K in cog_costs:
        net2, small_capacity = multiply_cognitive_cost(net, geom, thres, K)
        costs.append(net2[:,3])
    free_flow_OD_costs(net, costs, demand, output, verbose)


def LA_ue_K(factors, thres, cog_cost, output):
    '''
    parametric study for computing equilibrium flows with different demand factors
    and cognitive cost
    '''
    net, demand, node, geom = load_LA_3()
    demand[:,2] = demand[:,2] / 4000.
    net2, small_capacity = multiply_cognitive_cost(net, geom, thres, cog_cost)
    single_class_parametric_study(factors, output, net2, demand)


def LA_ue(factors, output):
    '''
    parametric study for computing equilibrium flows with different demand factors
    '''
    net, demand, node, geom = load_LA_3()
    demand[:,2] = demand[:,2] / 4000.
    single_class_parametric_study(factors, output, net, demand)

  
def LA_so(factors, output):
    '''
    parametric study for computing social optimum with different demand factors
    '''
    net, demand, node, geom = load_LA_3()
    demand[:,2] = demand[:,2] / 4000.
    net2 = net_with_marginal_cost(net)
    single_class_parametric_study(factors, output, net2, demand) 


def LA_od_costs(factors, output, verbose=0):
    '''
    compute the OD costs for UE, SO, and UE-K 
    where the cognitive cost is K=3000
    and with different demand: alpha * demand for demand in factors
    save OD costs into csv array with columns
    demand, X1_so, X1_ue_k, X1_ue, X2_so, X2_ue_k, X2_ue, ...
    '''
    net, demand, node, geom = load_LA_3()
    demand[:,2] = demand[:,2] / 4000.
    fs_so = np.loadtxt('data/LA/so_single_class.csv', delimiter=',', skiprows=1)
    fs_ue_k = np.loadtxt('data/LA/ue_k_single_class.csv', delimiter=',', skiprows=1)
    fs_ue = np.loadtxt('data/LA/ue_single_class.csv', delimiter=',', skiprows=1)
    costs = []
    for i in range(len(factors)):
        costs.append(cost(fs_so[:,i],net))
        costs.append(cost(fs_ue_k[:,i],net))
        costs.append(cost(fs_ue[:,i],net))
    free_flow_OD_costs(net, costs, demand, output, verbose)


def export_demand():
    net, demand, node, geom = load_LA_3()
    demand[:,2] = demand[:,2] / 4000.
    np.savetxt('data/LA/LA_demand.csv', demand, delimiter=',', header='O,D,flow', \
        comments='')


def LA_local_routed_costs(alphas, input, output):
    net, demand, node, features = load_LA_3()
    small_capacity = multiply_cognitive_cost(net, features, 1000., 3000.)[1]
    net_local = np.copy(net)
    for row in range(net.shape[0]):
        if small_capacity[row] == 0.0:
            net_local[row,3:] = net_local[row,3:] * 0.
    OD_non_routed_costs(alphas, net_local, net, demand, input, output, verbose=1)


def LA_local_non_routed_costs(alphas, input, output):
    net, demand, node, features = load_LA_3()
    net2, small_capacity = multiply_cognitive_cost(net, features, 1000., 3000.)
    net_local = np.copy(net)
    for row in range(net.shape[0]):
        if small_capacity[row] == 0.0:
            net_local[row,3:] = net_local[row,3:] * 0.
    OD_non_routed_costs(alphas, net_local, net2, demand, input, output, verbose=1)


def LA_parametric_study_3(alphas):
    g, d, node, feat = load_LA_3()
    d[:,2] = d[:,2] / 4000.
    parametric_study_2(alphas, g, d, node, feat, 1000., 3000., 'data/LA/test_{}.csv',\
        stop=1e-3)


def main():
    # process_LA_node()
    # process_LA_net()
    #visualize_LA_capacity()
    # visualize_LA_demand()
    # visualize_LA_result()
    # process_LA_od()
    # frank_wolfe_on_LA()
    # check_LA_result()
    # LA_parametric_study(.9)
    # LA_parametric_study_2(1.)
    # check__LA_connectivity()
    # remove_loops_in_LA_od()
    # reduce_demand()
    # load_LA_2()
    # LA_metrics(np.linspace(0,1,11), 'data/LA/test_{}.csv', 'data/LA/out.csv')
    # LA_metrics(np.linspace(0,1,11), 'data/LA/copy_2/test_{}.csv', \
    #     'data/LA/copy_2/out.csv')
    # LA_routed_costs(np.linspace(0,1,11), 'data/LA/test_{}.csv', \
    #     'data/LA/routed_costs.csv')
    # LA_routed_costs(np.linspace(0,1,11), 'data/LA/copy_2/test_{}.csv', \
    #     'data/LA/copy_2/routed_costs.csv')
    # LA_non_routed_costs(np.linspace(0,1,11), 'data/LA/test_{}.csv', \
    #     'data/LA/non_routed_costs.csv')    
    # LA_non_routed_costs(np.linspace(0,1,11), 'data/LA/copy_2/test_{}.csv', \
    #     'data/LA/copy_2/non_routed_costs.csv') 
    # total_link_flows(np.linspace(0,1,11), 'data/LA/test_{}.csv', 'data/LA/total_link_flows.csv')
    # visualize_LA_total_flows(10, only_local=True)
    # visualize_LA_flow_variation(only_local=False)
    # LA_free_flow_costs(1000., [3., 10., 30., 100., 300., 1000., 3000.])
    # LA_OD_free_flow_costs(1000., [1., 3., 10., 30., 100., 300., 1000., 3000.], \
    #     'data/LA/OD_free_flow_costs.csv', verbose=1)
    # LA_ue_K(np.linspace(.1,1,5), 1000., 3000., \
    #     'data/LA/ue_K_single_class.csv')
    # LA_ue(np.linspace(.1,1,5), 'data/LA/ue_single_class.csv')
    # LA_so(np.linspace(.1,1,5), 'data/LA/so_single_class.csv')
    # LA_od_costs(np.linspace(.1,1,5), 'data/LA/OD_costs.csv', verbose=1)
    # LA_local_routed_costs(np.linspace(0,1,11), 'data/LA/test_{}.csv', \
    #     'data/LA/local_routed_costs.csv')
    # LA_local_non_routed_costs(np.linspace(0,1,11), 'data/LA/test_{}.csv',\
    #     'data/LA/local_non_routed_costs.csv')
    # remove_doublons_in_LA_od()


    #=================================Attack================================
    LA_parametric_study_attack(.9,1000.,1.)

    #LA_metrics_attack(np.linspace(0,1,11), 'data/LA/test_{}.csv', 'data/LA/out_attack.csv',1.0)



    # ======================================================================

    # final scripts

    # LA_parametric_study_3(1.)

    # compute the OD costs under free-flow travel times and 
    # with different values of cognitive costs

    # LA_OD_free_flow_costs(1000., [1., 3., 10., 30., 100., 300., 1000., 3000.], \
    #     'data/LA/OD_free_flow_costs.csv', verbose=1)

    # ======================================================================

    # compute equilibria for single class games

    # LA_ue_K(np.linspace(.1,1,5), 1000., 3000., \
    #     'data/LA/ue_K_single_class.csv')
    # LA_ue(np.linspace(.1,1,5), 'data/LA/ue_single_class.csv')
    # LA_so(np.linspace(.1,1,5), 'data/LA/so_single_class.csv')

    # ======================================================================

    # compute the OD costs 

    # LA_od_costs(np.linspace(.1,1,5), 'data/LA/OD_costs.csv', verbose=1)

    # ======================================================================

    # compute general metrics such as VMT etc.

    # LA_metrics(np.linspace(0,1,11), 'data/LA/test_{}.csv', 'data/LA/out.csv')

    # ======================================================================

    # compute local and non-local routed and non-routed costs

    # export_demand()

    # LA_routed_costs(np.linspace(0,1,11), 'data/LA/test_{}.csv', \
    #     'data/LA/routed_costs.csv')    
    # LA_non_routed_costs(np.linspace(0,1,11), 'data/LA/test_{}.csv', \
    #     'data/LA/non_routed_costs.csv')  
    # LA_local_routed_costs(np.linspace(0,1,11), 'data/LA/test_{}.csv', \
    #     'data/LA/local_routed_costs.csv')
    # LA_local_non_routed_costs(np.linspace(0,1,11), 'data/LA/test_{}.csv',\
    #     'data/LA/local_non_routed_costs.csv')

if __name__ == '__main__':
    main()