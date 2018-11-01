from utils import strip
import os

class H1B:
	'''
	H1B class to count the number of certified occupations and states
	'''
	def __init__(self, filename):
		self.file = filename
		self.initialize_stats()


	def initialize_stats(self):
		'''
		initialization of needed parameters and dictionaries for
		occupation and state statistics
		'''
		self.status_num = 0
		self.occupation_dict = {}
		self.state_dict = {}


	@classmethod
	def fromFilename(cls, only_filename):
		'''
		initialize the class from the file name only, without os.path
		'''
		filename = os.getcwd() + '/input/' + only_filename
		try:
			os.path.isfile(filename)
			return cls(filename)
		else:
			print('Input File Not Found')
			return
		

	def record_title(self, row):
		'''
		loop over the titles once to find the corresponding indices
		some of the matching cases are hardcoded because the format 
		for each year might be different. it only searches for indices
		of visa status, applicant position and employer state.
		This runs in O(k) where k is number of columns.
		'''
		for j, title in enumerate(row):
			if title in ['CASE_STATUS', 'STATUS']:
				status_idx = j
			elif title in ['SOC_NAME', 'LCA_CASE_SOC_NAME']:
				occupation_idx = j
			elif title in ['WORKSITE_STATE', 'LCA_CASE_WORKLOC1_STATE']:
				state_idx = j
		return [status_idx, occupation_idx, state_idx]


	def record_line(self, row, indices, status):
		'''
		extract the occupation and state information from each line
		of input, store them into the dictionaries initialized in the class
		This runs in O(1), since it only get two items from list (ignoring strip)
		'''
		if len(row) <= indices[-1]:
			print('Warning: skipping one record because of incorrect format')
		elif row[indices[0]] == status:
			self.status_num += 1
			occ_key, state_key = strip(row[indices[1]]), strip(row[indices[2]])
			self.occupation_dict[occ_key] = self.occupation_dict.get(occ_key, 0) + 1
			self.state_dict[state_key] = self.state_dict.get(state_key, 0) + 1


	def read_file(self):
		'''
		main function that reads the file, extract information and
		records the statistics
		This runs in O(n), where n is the number of records
		'''
		with open(self.file) as f:
			idx = 0
			while True:
				## skipping the records where there is format error
				try:
					line = next(f)
				except StopIteration:
					break
				except:
					print('Warning: skipping one record because of incorrect format')
					continue

				line = line.split(';')

				if idx ==0:
					indices = self.record_title(line)
				else:
					try:
						self.record_line(line, indices, 'CERTIFIED')
					except:
						continue
				idx += 1
				
				if idx % 100000 == 0:
					print('Finished scanning {} records...'.format(idx))

	def output_TopN(self, stats_dict, filename, params_out, n):
		'''
		main function that outputs the needed files.
		'''
		if stats_dict =='occupation':
			sorted_stats = sorted(self.occupation_dict.items(), key=lambda x: (-x[1], x[0]))
		elif stats_dict == 'states':
			sorted_stats = sorted(self.state_dict.items(), key=lambda x: (-x[1], x[0]))
		else:
			print('No statistics found')
			return
		f = open(os.getcwd() + '/output/' + filename, 'w')
		## write column titles first
		f.write(';'.join(params_out) + '\n')
		## write the top N statistics
		for i in range(min(len(sorted_stats), 10)):
			percentage = ''.join([str(round(sorted_stats[i][1] * 100.0 / self.status_num, 1)), '%'])
			f.write(';'.join([str(c) for c in sorted_stats[i]] + [percentage]) + '\n')
		f.close()


if __name__ == '__main__':
	
	InputFile = 'h1bddd.csv'
	h1b = H1B.fromFilename(InputFile)
	print('Initialization completed ...')

	print('Start processing Statistics ...')
	h1b.read_file()
	print('Finished processing Statistics ...')

	print('Start Outputing ...')
	filenames = {'occupation': 'top_10_occupations.txt', 
					'states': 'top_10_states.txt'}
	params = {'occupation': ['TOP_OCCUPATIONS', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE'],
				'states': ['TOP_STATES', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE']}
	N = 10

	for stat in ['occupation', 'states']:
		h1b.output_TopN(stat, filenames[stat], params[stat], N)
		print('Done output {} ...'.format(stat))

	print('Finished All ...')
