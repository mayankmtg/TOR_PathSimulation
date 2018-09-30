import sys
import random
import matplotlib.pyplot as plt
import numpy as np

# Server desc processing

def serverdesc_process(file_name):
	server_desc_list = open(file_name,'r').read().split('@type server-descriptor 1.0')
	return server_desc_list

# Hash server_desc_list based in IP address
def serverdesc_hash(server_desc_list):
	server_desc_hash={}
	for server_desc in server_desc_list:
		for line in server_desc.split('\n'):
			if(line.startswith('router')):
				server_desc_hash[line.split()[2]]=server_desc
				break
	return server_desc_hash


def serverdesc_search(server_desc_hash, router_ip):
	if (router_ip in server_desc_hash):
		return server_desc_hash[router_ip]
	else:
		# print("NOT FOUND")
		return ""
	# for server_desc in server_desc_list:
	# 	for line in server_desc.split('\n'):
	# 		if(line.startswith('router')):
	# 			if(line.split()[2]==router_ip):
	# 				return server_desc
	# 			else:
	# 				break
	# # print("NOT FOUND")
	return ""

def serverdesc_family(found_server_desc):
	if(found_server_desc==""):
		return []
	for line in found_server_desc.split('\n'):
		if(line.startswith('family')):
			return line.split()[1:]
	return []
'''
def serverdesc_exitpolicy(found_server_desc):
	policy=[]
	for line in found_server_desc.split('\n'):
		if(line.startswith('reject') or line.startswith('accept')):
			policy.append(line)
	return policy
'''

# returns the input index dictionary and the input file with pointer incremented from head
def get_header_ind(input_file):
	head_index={}
	for line in input_file:
		header_array=line.split(',')
		ind=0
		for h in header_array:
			head_index[h]=ind
			ind+=1
		break
	return head_index, input_file

# return all the relays in file in list format
def get_relay_list(input_file):
	relay_list=[]
	for line in f:
		relay_list.append(line.split(','))
	return relay_list


# Get weights from global consensus
def get_bandwidth_weights(input_file):
	b_weights={}
	for line in input_file:
		if line.split()[0]=='bandwidth-weights':
			line_array=line.split()
			for i in line_array:
				if '=' in i:
					m=i.split('=')
					b_weights[m[0]]=int(m[1])
			break
	return b_weights

def get_flag_set(relay_list, head_index, flag_name, comparator):
	f_ind = head_index[flag_name]
	# print("FLAG_IND: "),
	# print(f_ind)
	guard_list=[]
	for i in relay_list:
		if ( i[f_ind] == comparator ):
			guard_list.append(i)
	return set(map(tuple,guard_list))

# assuming that the relay list is filtered base on some configurations
# TODO: set configurations to filter relay list
# pos character are among g,m,e which form second weight character
def bandwidth_selection_algorithm(relay_list, head_index, b_weights, pos):
	bw_ind = head_index['ConsensusBandwidth']
	e_flag = head_index['Flag - Exit']
	g_flag = head_index['Flag - Guard']
	be_flag= head_index['Flag - Bad Exit']
	
	# B=0
	# Be=0
	# Bg=0
	# q=len(relay_list)

	# for relay in relay_list:
	# 	B+=int(relay[bw_ind])
	# 	if(relay[e_flag]=='1' and relay[be_flag]=='0'):
	# 		Be+=int(relay[bw_ind])
	# 	if(relay[g_flag]=='1'):
	# 		Bg+=int(relay[bw_ind])
	
	total_bw=0
	for relay in relay_list:
		if(relay[be_flag]=='0' and relay[e_flag]=='1' and relay[g_flag]=='1'):
			bw=int(relay[bw_ind]) * int(b_weights['W'+pos+'d'])
		elif(relay[g_flag]=='1'):
			bw=int(relay[bw_ind]) * int(b_weights['W'+pos+'g'])
		elif(relay[e_flag]=='1' and relay[be_flag]=='0'):
			bw=int(relay[bw_ind]) * int(b_weights['W'+pos+'e'])
		else:
			bw=int(relay[bw_ind])
		
		total_bw+=bw
	random_bw=random.randint(1,int(total_bw))
	temp=0
	for relay in relay_list:
		if(relay[be_flag]=='0' and relay[e_flag]=='1' and relay[g_flag]=='1'):
			temp+=int(relay[bw_ind]) * int(b_weights['W'+pos+'d'])
		elif(relay[g_flag]=='1'):
			temp+=int(relay[bw_ind]) * int(b_weights['W'+pos+'g'])
		elif(relay[e_flag]=='1' and relay[be_flag]=='0'):
			temp+=int(relay[bw_ind]) * int(b_weights['W'+pos+'e'])
		else:
			temp+=int(relay[bw_ind])
		if(temp > random_bw):
			return relay
	
	print("Relay not found")
	# else return any random node
	return relay_list[random.randint(1,q)]


def check_constraints(relay1,server_desc1,relay2,server_desc2,head_index):
	ip_ind = head_index['IP Address']
	if( relay1[ip_ind] == relay2[ip_ind] ):
		return False
	elif( set(serverdesc_family(server_desc1)) & set(serverdesc_family(server_desc2)) != set([]) ):
		# TODO: confirm family constraints
		return False
	elif( relay1[ip_ind].split('.')[:2] == relay2[ip_ind].split('.')[:2] ):
		# TODO: Confirm check for /16 subnet
		return False
	else:
		return True

def add_indices(relay_list, head_index):
	for i in range(len(relay_list)):
		relay_list[i].append(i)
	head_index['index'] = head_index['OrAddress\n']+1
	random.shuffle(relay_list)
	return relay_list[:200], head_index

def compromise_list(no_of_relays, n):
	rand_list = random.sample(range(no_of_relays),n)
	return rand_list

def exp_func(x):
	return 10000*np.power(x/6367.0,2)
# MAIN METHOD


head_index={}
relay_list=[]
with open(sys.argv[1]) as f:
	
	head_index, f = get_header_ind(f)
	
	relay_list = get_relay_list(f)
	# print(head_index)
	# print(len(relay_list))

b_weights={}
with open('./consensus') as f:
	b_weights = get_bandwidth_weights(f)

server_desc_list =  serverdesc_process('./server_desc')
server_desc_hash = serverdesc_hash(server_desc_list)



# TODO:
# we don't build circuits until we have enough directory information
	# Having a consensus that's been valid at some point in thelast REASONABLY_LIVE_TIME interval (24 hourts).
	# Having enough descriptors that we could build at least somefraction F of all bandwidth-weighted paths, without takingExitNodes/EntryNodes/etc into account.
		# (F is set by the PathsNeededToBuildCircuits option,defaulting to the 'min_paths_for_circs_pct' consensusparameter, with a final default value of 60%.)
	# Having enough descriptors that we could build at least somefraction F of all bandwidth-weighted paths, _while_ takingExitNodes/EntryNodes/etc into account.
		# (F is as above.)
	# Having a descriptor for every one of the firstNUM_GUARDS_TO_USE guards among our primary guards. (seeguard-spec.txt)

# TODO:
# pre-emtive circuit creation algorithm
	# scan through the list of last used ports and create circuits that support those ports

# TODO:
# create circuits according to client demands

# Path selection and constraints
#  This section contains most of the details of path creation algorithm used by TOR


# CLIENT SIDE OPERATIONS

# Circuit length chosen: 3



relay_list, head_index=add_indices(relay_list,head_index)
# for l in relay_list:
# 	print l
# 	break
# print(head_index)




valid_set = get_flag_set(relay_list,head_index,'Flag - Valid','1')
running_set = get_flag_set(relay_list,head_index, 'Flag - Running', '1')
stable_set = get_flag_set(relay_list,head_index, 'Flag - Stable', '1')
fast_set = get_flag_set(relay_list,head_index, 'Flag - Fast', '1')

# Assumption: The client is configured to select all the circuits that are stable, valid, fast and running
# All other possible configurations can be set using the following operation only
config_set = running_set & stable_set & valid_set & fast_set

print("PATH CREATION")
exit_set = get_flag_set(relay_list,head_index,'Flag - Exit', '1')
goodExit_set = get_flag_set(relay_list, head_index, 'Flag - Bad Exit', '0')
possible_exit = exit_set & goodExit_set & config_set

guard_set = get_flag_set(relay_list, head_index, 'Flag - Guard', '1')
possible_guard = guard_set & config_set

possible_middle=set(map(tuple,relay_list)) & fast_set & running_set

n_paths=10000
path_circuits=[]

for i in range(n_paths):
	# EXIT-NODE
	chosen_exit = bandwidth_selection_algorithm(list(possible_exit), head_index, b_weights, 'e')
	exit_server_desc = serverdesc_search(server_desc_hash,chosen_exit[head_index['IP Address']])

	# GUARD-NODE
	chosen_guard = bandwidth_selection_algorithm(list(possible_guard), head_index, b_weights, 'g')
	guard_server_desc = serverdesc_search(server_desc_hash,chosen_guard[head_index['IP Address']])

	while(not(check_constraints(chosen_exit,exit_server_desc, chosen_guard, guard_server_desc, head_index ))):
		chosen_guard = bandwidth_selection_algorithm(list(possible_guard), head_index, b_weights, 'g')
		guard_server_desc = serverdesc_search(server_desc_hash,chosen_guard[head_index['IP Address']])

	# MIDDLE-NODE
	chosen_middle = bandwidth_selection_algorithm(list(possible_middle), head_index, b_weights, 'm')
	middle_server_desc = serverdesc_search(server_desc_hash,chosen_middle[head_index['IP Address']])

	while(not(check_constraints(chosen_exit,exit_server_desc, chosen_middle, middle_server_desc, head_index ))
		and not(check_constraints(chosen_guard,guard_server_desc, chosen_middle, middle_server_desc, head_index ))):
		chosen_middle = bandwidth_selection_algorithm(list(possible_middle), head_index, b_weights, 'm')
		middle_server_desc = serverdesc_search(server_desc_hash,chosen_middle[head_index['IP Address']])
	index_ind=head_index['index']
	path_circuits.append({
		'X':chosen_exit[index_ind],
		'M':chosen_middle[index_ind],
		'G':chosen_guard[index_ind]
	})
	# print(chosen_exit)
	# print()
	# print(chosen_guard)
	# print()
	# print(chosen_middle)
print(len(path_circuits))

# ex_counter={}
# for i in path_circuits:
# 	key=str(i['G'])+'_'+ str(i['X'])
# 	if ( key in ex_counter ):
# 		ex_counter[key]+=1
# 	else:
# 		ex_counter[key]=1

x_array=[]
y_array=[]
for n_compromised_nodes in range(1,len(relay_list)):
	comp_list=compromise_list(len(relay_list), n_compromised_nodes)
	ones_list=[1 for i in range(len(comp_list))]
	comp_hash=dict(zip(comp_list,ones_list))
	n_compromised_paths=0
	for path in path_circuits:
		try:
			# if(path['X'] in comp_list and path['G'] in comp_list):
			x=comp_hash[path['X']]
			y=comp_hash[path['G']]
			n_compromised_paths+=1
		except KeyError:
			pass

	x_array.append(n_compromised_nodes)
	y_array.append(n_compromised_paths)

# exp_array=map(exp_func,np.array(x_array))
plt.plot(x_array, y_array, 'r-')
# plt.plot(x_array, exp_array, 'b')
# print(exp_array)
# print(x_array)
plt.show()










