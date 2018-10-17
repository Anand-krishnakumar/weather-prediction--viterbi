
def HMM():
	b1 = {(1, "HOT"): 0.2, (2, "HOT"): 0.4, (3, "HOT"): 0.4}
	b2 = {(1, "COLD"): 0.5, (2, "COLD"): 0.4, (3,"COLD"): 0.1}
	transitions  = {("HOT", "HOT"): 0.7, ("HOT", "COLD"): 0.3, ("COLD", "COLD"): 0.6, ("COLD", "HOT"): 0.4}
	pi = {"HOT": 0.8, "COLD": 0.2}
	return b1, b2, transitions, pi

def viterbi(b1, b2, transitions, pi, seq):
	vHOT, vCOLD, pHOT, pCOLD = [], [], [], []
	result = []
	sequence = [int(i) for i in str(seq)]
	length = len(sequence)-1
	v11 = pi["HOT"]*b1[(sequence[0], "HOT")]
	v12 = pi["COLD"]*b2[(sequence[0], "COLD")]

	pHOT.append(v11)
	pCOLD.append(v12)

	vHOT.append((sequence[0], v11, "HOT"))
	vCOLD.append((sequence[0], v12, "COLD"))

	for i in range(1, len(sequence)):
		h_h = pHOT[i-1] * transitions[("HOT", "HOT")] * b1[(sequence[i], "HOT")]
		c_h = pCOLD[i-1] * transitions[("COLD", "HOT")] * b1[(sequence[i], "HOT")]
		h_c = pHOT[i-1] * transitions[("HOT", "COLD")] * b2[(sequence[i], "COLD")]
		c_c = pCOLD[i-1] * transitions[("COLD", "COLD")] * b2[(sequence[i], "COLD")]

		bestHOT = max(h_h, c_h)
		bestCOLD = max(h_c, c_c)

		pHOT.append(bestHOT)
		pCOLD.append(bestCOLD)

		if bestHOT == h_h:
			vHOT.append((sequence[i], bestHOT, "HOT"))
		else:
			vHOT.append((sequence[i], bestHOT, "COLD"))
		if bestCOLD == h_c:
			vCOLD.append((sequence[i], bestCOLD, "HOT"))
		else:
			vCOLD.append((sequence[i], bestCOLD, "COLD"))
	if vHOT[length][1] > vCOLD[length][1]:
		result.append(vHOT[length][2])
		prev = vHOT[length][2]
	else:
		result.append(vCOLD[length][2])	
		prev = vCOLD[length][2]
	length -= 1
	while (length > 0):
		if prev == "HOT":
			result.append(vHOT[length][2])
			prev = vHOT[length][2]
		else:
			result.append(vCOLD[length][2])
			prev = vCOLD[length][2]
		length -= 1
	result = result[::-1]
	return result, vHOT, vCOLD


			


if __name__ == "__main__":
	seq1 = 331122313
	seq2 = 331123312
	b1, b2, transitions, pi = HMM()
	result1, vHOT1, vCOLD1 = viterbi(b1, b2, transitions, pi, seq1)
	result2, vHOT2, vCOLD2 = viterbi(b1, b2, transitions, pi, seq2)

	print("The weather prediction for the sequence ", seq1, "is ", result1)
	print("The weather prediction for the sequence ", seq2, "is ", result2)
	
	