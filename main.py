import sys
import random

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
	g_ind = head_index[flag_name]
	print("G_IND: "),
	print(g_ind)
	guard_list=[]
	for i in relay_list:
		if ( i[g_ind] == comparator ):
			guard_list.append(i)
	return set(guard_list)

# assuming that the relay list is filtered base on some configurations
# TODO: set configurations to filter relay list
# pos character are among g,m,e which form second weight character
def bandwidth_selection_algorithm(relay_list, head_index, b_weights, pos):
	bw_ind = head_index['Bandwidth (KB/s)']
	e_flag = head_index['Flag - Exit']
	g_flag = head_index['Flag - Guard']
	be_flag= head_index['Flag - Bad Exit']
	
	B=0
	Be=0
	Bg=0
	q=len(relay_list)

	for relay in relay_list:
		B+=int(relay[bw_ind])
		if(relay[e_flag]=='1' and relay[be_flag]=='0'):
			Be+=int(relay[bw_ind])
		if(relay[g_flag]=='1'):
			Bg+=int(relay[bw_ind])
	
	total_bw=0
	for relay in relay_list:
		if(relay[be_flag]=='0' and relay[e_flag]=='1' and relay[g_flag]=='1'):
			bw=relay[bw_ind] * b_weights['W'+pos+'d']
		elif(relay[g_flag]=='1'):
			bw=relay[bw_ind] * b_weights['W'+pos+'g']
		elif(relay[e_flag]=='1' and relay[be_flag]=='0'):
			bw=relay[bw_ind] * b_weights['W'+pos+'e']
		else:
			bw=relay[bw_ind]
		
		total_bw+=bw
	random_bw=random.randint(1,int(total_bw))
	temp=0
	for relay in relay_list:
		if(relay[be_flag]=='0' and relay[e_flag]=='1' and relay[g_flag]=='1'):
			temp+=relay[bw_ind] * b_weights['W'+pos+'d']
		elif(relay[g_flag]=='1'):
			temp+=relay[bw_ind] * b_weights['W'+pos+'g']
		elif(relay[e_flag]=='1' and relay[be_flag]=='0'):
			temp+=relay[bw_ind] * b_weights['W'+pos+'e']
		else:
			temp+=relay[bw_ind]
		if(temp > random_bw):
			return relay

	# else return any random node
	return relay_list[random.randint(1,q)]

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

exit_set = get_flag_set(relay_list,head_index,'Flag - Exit', '1')
goodExit_set = get_flag_set(relay_list, head_index, 'Flag - Bad Exit', '0')

valid_set = get_flag_set(relay_list,head_index,'Flag - Valid','1')







