folder=hmm_train_folder

help:
	@echo -e "Usage" 
	@echo -e "Contact Murugesan for futher"
train: train_monophones
	@echo -e "\n>> we will only train monophones, see train_triphones make cmd  otherwise\n"

train_monophones:
	@echo -e "*** Training the HMMs with HTK ***"
	@echo -e "using the folder $(dataset_train_folder)"
	@echo -e "\n>>> Preparing the HMM model \n"
	mkdir -p $(folder)
	cp $(dataset_train_folder)/labels $(folder)/monophones0