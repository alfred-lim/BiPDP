# Author: Alfred Lim
# Location: Singapore
# Date: 2021-11-27
# Task: create reading (O2P) model on Lens
# Data: Lim, O'Brien, & Luca (submitted) word dataset

## Set size of layers (number of units)
# Hidden layer
set hiddenSize 100 
# Ortho layer
set inputSize  260 
# Phon layer
set outputSize 224
# Cleanup layer 
set cleanSize  50  

## Set up model
# Create continuous network  with 4 time intervals and 3 ticks per interval (total 12 ticks)
addNet reading_mod -i 4.0 -t 3 CONTINUOUS	

## Add layers (all layers use input integration and cross entropy)
# Add Orth layer (no biased unit, can receive input and produce output, and inputs can be clamped)
addGroup Orth  $inputSize    -BIASED INPUT OUTPUT CROSS_ENTROPY SOFT_CLAMP IN_INTEGR
# Add Hidden layer (no biased unit)
addGroup HiddenOPPO $hiddenSize  -BIASED IN_INTEGR
# Add Phon layer (no biased unit, can receive input and produce output, and inputs can be clamped)
addGroup Phon $outputSize  -BIASED INPUT OUTPUT CROSS_ENTROPY SOFT_CLAMP IN_INTEGR
# Add Orth-cleanup layer (no biased unit)
addGroup CleanupO  $cleanSize   -BIASED IN_INTEGR
# Add Phon-cleanup layer (no biased unit)
addGroup CleanupP  $cleanSize   -BIASED IN_INTEGR

## Add bi-directional connections between layers
# Between Orth, Hidden, and Phon layers (mean weights is 0)
connectGroups   Orth HiddenOPPO Phon -bi -mean 0 -range 0.5
# Between Orth and Orth-cleanup layer (mean weights is 0)
connectGroups   Orth CleanupO -bi -mean 0 -range 0.5
# Between Orth and Phon-cleanup layer (mean weights is 0)
connectGroups   Phon CleanupP -bi -mean 0 -range 0.5

## Set up training dataset
# Load example file then name the dataset as OP_training
loadExamples OP.ex -s OP_training
# Delay between onset of Input (Orth) and Output (Phon) - total 6 ticks
setObj OP_training.graceTime 2.0
# Event last for full 4 time intervals (prevent early termination) - total 12 ticks
setObj OP_training.minTime   4.0
# Event last for full 4 time intervals (prevent early termination) - total 12 ticks
setObj OP_training.maxTime   4.0
# Training examples are selected based on their frequency (probabilistic)
exampleSetMode OP_training PROBABILISTIC


## Set up testing dataset
# Load example file then name the dataset as OP_testing
loadExamples OP.ex -s OP_testing
# Delay between onset of Input (Orth) and Output (Phon) - total 6 ticks
setObj OP_testing.graceTime 2.0
# Event last for full 4 time intervals (prevent early termination) - total 12 ticks
setObj OP_testing.minTime   4.0
# Event last for full 4 time intervals (prevent early termination) - total 12 ticks
setObj OP_testing.maxTime   4.0
# Testing examples are selected in the order in which they were read from the example file
exampleSetMode OP_testing ORDERED

## Set model parameters
# Momentum descent
setObj 	momentum          	0.8	
# Scales the weight deltas (changes)	
setObj 	learningRate        0.5000	
# Set default training epoch
set 	tillUpdates 		1 	
# Set SOFT_CLAMP strength to max	
setObj 	clampStrength   	1.0     
# Simply scale the error and output derivatives by the example frequency (i.e. pseudo-frequencies)
setObj 	pseudoExampleFreq 	1   
# Encourage units to have binary outputs    
setObj  outputCostStrength 	0.1 	
# When testing, an example is considered correct if all units is within this range to target value
setObj  testGroupCrit      	0.25
# Report network progress every 1 epoch	
setObj  reportInterval     	1       

# Define function to launch clients
proc launchClients {numClient} {
	lens
}

# Define function to set training data for all clients (for parallel training)
proc setAllTrainingSet { setName } {
	useTrainingSet $setName
	sendEval "useTrainingSet $setName"
}

# Define function to set testing data for all clients (for parallel training)
proc setAllTestingSet { setName } {
	useTestingSet $setName
	sendEval "useTestingSet $setName"
}

## Init stop-training variable
set stop 0

## Define custom training function
proc trainParallel2 { tillUpdates } {
	## Declare variables for training
	set toWeightCount 100 	#save weight every 100 epochs
	set toTestCount 100 	#test model every 100 epochs
	set toOutCount 1000 	#save all layers activity for MSE calculation later
	setAllTrainingSet "OP_training" 	#set training set to be used
	setAllTestingSet "OP_testing"		#set testing set to be used
	set fullTestingSet consistLH_b10_test               #
	set fFull [open "testLog_full_reading.txt" "a"] 	#set accuracy output filename to store accuracy per testing
	upvar 1 stop stop 		#set as global variable
	upvar 1 Test Test  		#set as global variable
	
	## Create accuracy output file
	puts $fFull "[getObj trainingSet.name] $fullTestingSet [getObj learningRate] $tillUpdates"
	puts $fFull "mode batchNum totalUpdates numExamples numTicks totalError exampleError tickError totalCost tickCost examplesCorrect percentCorrect sysTime"
	close $fFull
	
	## Training loop - loop for X epochs
	for {set i [getObj totalUpdates]} {$i < $tillUpdates} {incr i} {
		# Perform training and report its outcome to console
		trainParallel 1 -report 1
		
		# Check if it's the right epoch to perform testing
		if { [getObj totalUpdates] % $toTestCount == 0} {
			# Store system time
			set systemTime [clock seconds]
			
			# Check if it's the right epoch to save all layers activity
			if { [getObj totalUpdates] % $toOutCount == 0} {
				# Create file to store all layers activity
				puts "Compressing testOut_[getObj trainingSet.name]_[getObj testingSet.name]_ep[getObj totalUpdates].txt..."
				openNetOutputFile "out/testOut_[getObj trainingSet.name]_&[getObj testingSet.name]_ep[getObj totalUpdates].txt"
				# Perform testing
				test -r
				# Close file after writing
				closeNetOutputFile
				# Compress file to save storage space
				exec 7z a out/testOut_[getObj trainingSet.name]_&[getObj testingSet.name]_ep[getObj totalUpdates].7z out/testOut_[getObj trainingSet.name]_&[getObj testingSet.name]_ep[getObj totalUpdates].txt 
				# Remove the uncompressed raw file to save storage space
				file delete "out/testOut_[getObj trainingSet.name]_&[getObj testingSet.name]_ep[getObj totalUpdates].txt"
			} else {
				# Perform testing only otherwise
				test -r
			}
			# Retrieve testing outcome from the internal array
			array set Test_OP [array get Test]

			# Open test log file for writing
			set fFull [open "testLog_full_reading.txt" "a"]
			# Write testing outcome
			puts $fFull "op $batchCount [getObj totalUpdates] $Test(numExamples) $Test(numTicks) $Test(totalError) $Test(exampleError) $Test(tickError) $Test(totalCost) $Test(tickCost) $Test(examplesCorrect) $Test(percentCorrect) [clock seconds]"
			# Close file after writing
			close $fFull
			
			# Check if overall accuracy is greater than 90%
			if { [expr ($Test_OP(percentCorrect))] >= 90} {
				# Save model weights file and stop training
				saveWeights "wt/consistLH_b$batchCount\_ep[getObj totalUpdates].wt"
				set stop 1
			}
		}
		
		# Check if it's the right epoch to save model weights file
		if { [getObj totalUpdates] % $toWeightCount == 0 } {
			saveWeights "wt/consistLH_b$batchCount\_ep[getObj totalUpdates].wt"
		}

		# Check if user wants to terminate training
		if { $stop == 1 } {
			break
			puts "Terminated by user..."
		}
	}
}