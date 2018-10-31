from utils import strip
import os

class H1B:
	def __init__(self, filename):
		self.file = filename
		self.initialize_stats()

	def initialize_stats(self):
		self.certify_num = 0
		self.occupation_dict = {}
		self.state_dict = {}

	def read_file(self):
		with open(self.file) as f:
			for idx, line in enumerate(f):
				row = line.split(';')
				if idx == 0:
					## loop over the titles once to find the corresponding indices
					for j, title in enumerate(row):
						if title == 'CASE_NUMBER':
							case_idx = j
						elif title == 'CASE_STATUS':
							certify_idx = j
						elif title == 'SOC_NAME':
							occupation_idx = j
						elif title == 'WORKSITE_STATE':
							state_idx = j
				elif row[certify_idx] == 'CERTIFIED':
					self.certify_num += 1
					occ_key, state_key = strip(row[occupation_idx]), strip(row[state_idx])
					self.occupation_dict[occ_key] = self.occupation_dict.get(occ_key, 0) + 1
					self.state_dict[state_key] = self.state_dict.get(state_key, 0) + 1

	def output_TopN(self, n, parent):
		occupation_sorted = sorted(self.occupation_dict.items(), key=lambda x: (-x[1], x[0]))
		state_sorted = sorted(self.state_dict.items(), key=lambda x: (-x[1], x[0]))

		f = open(parent + '/output/top_10_occupations.txt', 'w')
		f.write(';'.join(['TOP_OCCUPATIONS', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE']) + '\n')
		for i in range(min(len(self.occupation_dict), 10)):
			percentage = ''.join([str(round(occupation_sorted[i][1] * 100.0 / self.certify_num, 1)), '%'])
			f.write(';'.join([str(char) for char in occupation_sorted[i]] + [percentage]) + '\n')
		f.close()


		f = open(parent + '/output/top_10_states.txt', 'w')
		f.write(';'.join(['TOP_STATES', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE']) + '\n')
		for i in range(min(len(self.state_dict), 10)):
			percentage = ''.join([str(round(state_sorted[i][1]  * 100.0 / self.certify_num, 1)), '%'])
			# percentage = str(round(state_sorted[i][1] * 100.0 / self.certify_num, 1))
			f.write(';'.join([str(char) for char in state_sorted[i]] + [percentage]) + '\n')
		f.close()


if __name__ == '__main__':
	parent_dir = os.getcwd()
	filename = parent_dir + '/input/h1b_input.csv'
	h1b = H1B(filename)
	h1b.read_file()
	h1b.output_TopN(10, parent_dir)