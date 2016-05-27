__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

'''
Some function that can be useful
'''

import numpy as np


def digits(x):
    # return number of digits in the integer part
    if x < 10.0: return 1
    return int(np.log(x)/np.log(10)) + 1


def spaces(n):
    # return the appropriate number of spaces
    return ''.join([' ']*(n))


def multiply_cognitive_cost(net, feat, thres, cog_cost):
    '''
    given a numpy array 'net' of the form [[link_id, from, to, a0, a1, ..]]
    and numpy array 'feat' containing [[capacity, length, FreeFlowTime]]
    multiply all coefficients a0, a1, .. by a factor 'cog_cost'
    if capcacity in feat under a threshold
    '''
    net2 = np.copy(net)
    small_capacity = np.zeros((net2.shape[0],))
    for row in range(net2.shape[0]):
        if feat[row,0] < thres:
            small_capacity[row] = 1.0
            net2[row,3:] = net2[row,3:] * cog_cost
    return net2, small_capacity


def modify_capacity(net, links_affected, beta):
    '''
    given a numpy array 'net' of the form [[link_id, from, to, a0, a1, ..]]
    and given a list of booleans such that 'links_affected'
    multiply the capcacity of links with entry True in 'links_affected' by beta
    equivalent to dividing the coefficients a1,a2,... by beta^1,beta^2,...
    '''
    net2 = np.copy(net)
    for row in range(net2.shape[0]):
        if links_affected[row]:
            for j in range(4,net2.shape[1]):
                net2[row,j] = net2[row,j] / (beta**(j-3))
    return net2


def heterogeneous_demand(d, alpha):
    d_nr = np.copy(d)
    d_r = np.copy(d)
    d_nr[:,2] = (1-alpha) * d_nr[:,2]
    d_r[:,2] = alpha * d_r[:,2]
    return d_nr, d_r


def braess_heterogeneous(demand_r, demand_nr):
    # generate heteregenous game on Braess network
    g2 = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
    g1 = np.copy(g2)
    g1[2,3] = 1e8
    d1 = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
    d1=np.reshape(d1, (1,3))
    d1[0,2] = demand_nr
    d2 = np.copy(d1)
    d2[0,2] = demand_r
    return g1, g2, d1, d2


def net_with_marginal_cost(net):
    '''
    from net = [[link_id, from, to, a0, a1, a2, ...]]
    compute network with marginal costs 
    net = [[link_id, from, to, a0, a1 + a1, a2 + 2*a2, a3 + 3*a3, ...]]
    '''
    degree = net.shape[1] - 4
    net2 = np.copy(net)
    for i in range(degree+1):
        net2[:,i+3] = net[:,i+3] * (1.+i)
    return net2


def orientation(p, q, r):
    '''
    returns 0 if p, q, and r are colinear
    return 1 if clockwise
    return 2 if counterclockwise
    '''
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0: return 0
    if val > 0: return 1
    return 2


def onSegment(p, q, r):
    '''
    given three colinear points p, q, r, the function checks if
    point q lies on line segment 'pr'
    '''
    return (q[0] <= max(p[0], r[0])) \
        and (q[0] >= min(p[0], r[0])) \
            and (q[1] <= max(p[1], r[1])) \
            and (q[1] >= min(p[1], r[1]))


def doIntersect(p1, q1, p2, q2):
    '''
    return true if line segment p1q1 and p2q2 intersect
    '''
    # find the four orientations needed for general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # general case
    if (o1 != o2) and (o3 != o4): return True

    # special cases
    # p1, q1, and p2 are colinear and p2 lies on segment p1q1
    if (o1 == 0) and onSegment(p1, p2, q1): return True
    # p1, q1 and p2 are colinear and q2 lies on segment p1q1
    if (o2 == 0) and onSegment(p1, q2, q1): return True
    # p2, q2 and p1 are colinear and p1 lies on segment p2q2
    if (o3 == 0) and onSegment(p2, p1, q2): return True
    # p2, q2 and q1 are colinear and q1 lies on segment p2q2
    if (o4 == 0) and onSegment(p2, q1, q2): return True

    return False


def isInside(polygon, n, p, infinity=10e8):
    '''
    Returns True if the point p lies inside the polygon[] with n vertices
    '''
    # there must be at least 3 vertices in polygon
    if n < 3: return False
    # Create a point for line segment from p to infinite
    extreme = [infinity, p[1]]
    # count intersections of the above line with sides of polygon
    count = 0
    for i in range(n):
        next = (i+1)%n
        # Check if the line segment from 'p' to 'extreme' intersects
        # with the line segment from 'polygon[i]' to 'polygon[next]'
        if doIntersect(polygon[i], polygon[next], p, extreme):
            # If the point 'p' is colinear with line segment 'i-next',
            # then check if it lies on segment. If it lies, return true,
            # otherwise false
            if orientation(polygon[i], p, polygon[next]) == 0:
                return onSegment(polygon[i], p, polygon[next])
            count = count + 1
    return (count%2 == 1)


def isInsideBox(box, p):
    '''
    Returns True if the point p lies inside the box
    box = [p,q]
    '''
    return (p[0] <= max(box[0][0], box[1][0])) \
        and (p[0] >= min(box[0][0], box[1][0])) \
            and (p[1] <= max(box[0][1], box[1][1])) \
            and (p[1] >= min(box[0][1], box[1][1]))


def areInside(polygon, n, ps, infinity=10e8):
    '''
    Returns a list of 1 or 0 depending on whether point p in ps
    is inside the polygon or not
    '''
    tmp = np.array(polygon)
    # bounding box for the polygon
    box = [[min(tmp[:,0]), min(tmp[:,1])],[max(tmp[:,0]), max(tmp[:,1])]]
    out = []
    # check if each point is inside the polygon
    for p in ps:
        # check if the point is inside the bounding box
        if isInsideBox(box, p):
            if isInside(polygon, n, p, infinity=infinity):
                out.append(1)
            else:
                out.append(0)
        else:
            out.append(0)
    return out

