import sys



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


# MAIN METHOD

with open(sys.argv[1]) as f:
	
	head_index, f = get_header_ind(f)
	
	relay_list = get_relay_list(f)
	# print(head_index)
	# print(len(relay_list))


with open('./consensus') as f:
	# print(get_bandwidth_weights(f))





