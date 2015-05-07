##################################################
######scikit_learn to do the classifications######
##################################################
##################################################
from time import sleep
from sklearn import svm
from sklearn import cross_validation
from sklearn import metrics
import numpy as np
##################################################
#####Hard coded (currently) where the datasets####
#################are located######################
##################################################

file_a0 = "a0.txt"
file_a1 = "a1.txt"
file_a2 = "a2.txt"
file_a3 = "a3.txt"
file_a4 = "a4.txt"
file_a5 = "a5.txt"
file_a6 = "a6.txt"
file_a7 = "a7.txt"
file_a8 = "a8.txt"
file_a9 = "a9.txt"

format_a = [file_a0,file_a1,file_a2,file_a3,file_a4,file_a5,file_a6,file_a7,file_a8,file_a9]

file_n0 = "n0.txt"
file_n1 = "n1.txt"
file_n2 = "n2.txt"
file_n3 = "n3.txt"
file_n4 = "n4.txt"
file_n5 = "n5.txt"
file_n6 = "n6.txt"
file_n7 = "n7.txt"
file_n8 = "n8.txt"
file_n9 = "n9.txt"

format_n = [file_n0,file_n1,file_n2,file_n3,file_n4,file_n5,file_n6,file_n7,file_n8,file_n9]

file_v0 = "v0.txt"
file_v1 = "v1.txt"
file_v2 = "v2.txt"
file_v3 = "v3.txt"
file_v4 = "v4.txt"
file_v5 = "v5.txt"
file_v6 = "v6.txt"
file_v7 = "v7.txt"
file_v8 = "v8.txt"
file_v9 = "v9.txt"

total_percent = 0
format_v = [file_v0,file_v1,file_v2,file_v3,file_v4,file_v5,file_v6,file_v7,file_v8,file_v9]
format_index = 0
binary_array = list()
cur_scores   = list()
new_cur = 0
format_array = []


for i in range(0,4000000):
   format_array.extend('0')


def roc_config(fileName,type_):
    if isinstance(fileName,str):
        my_file = open(str(fileName),"r+")
        words = my_file.read().split("\n")
        my_file.close()
        words.remove('')
        find_new = 0
        ret_ = list()
        for word in words:
            if word == 'new':
                words[find_new] = type_
                ret_.append(type_)
    return ret_ 
##################################################
####Create the instances for validation testing###
##################################################
##################################################

def makeValidationInstance(fileName,f_index):
    if isinstance(fileName,str):
        my_file = open(str(fileName),"r+")
        words = my_file.read().split("\n")
        my_file.close()
        words.remove('')
        
        num_instances = words.count("new")
        print("Number of Instances to Validate: " + str(num_instances))
     
        instance = []
        data = []
        for line in words:
            if line == "new":    
                my_data = [data]           
                instance += (my_data)
                data = []
            data.extend([line.split()])
            
        for i in instance:
            for entry in i:
                if '1' in entry:
                    entry.remove('1')
		    format_array[f_index] = '1'
		    f_index += 1
                if '0' in entry:
                    entry.remove('0')
		    f_index += 1
        return instance    
    else:
        return -1

##################################################
#####Create the instances for training############
##################################################
##################################################

def makeFitInstance(fileName):
    if isinstance(fileName, str):
        my_file = open(str(fileName), "r+")
        words = my_file.read().split("\n")
        my_file.close()
        words.remove('')
    
        data = []
        for line in words:
            data.extend([line.split()])
    
        classi = []
        for entry in data:
            if entry[-1] == '1':
                classi.extend('a')
                entry.remove('1')
            elif entry[-1] == '0':
                classi.extend('n')
                entry.remove('0')         
        instance = {}
        instance[0] = data
        instance[1] = classi
        return instance
    else:
        return -1
    
##################################################
#######Calculates the class of the subsequences###
########as a ratio################################
##################################################

def calClass(svm,data,cur_scores,new_cur):
    ret_ = dict()
    print("begin calClass cur_ is: " + str(new_cur))
    if new_cur is 1:
	cur_scores = list()
        new_cur = 0
    normal = ['n']
    attack = ['a']
    num = 0
    total_n = 0
    total_a = 0
    if ['new'] in data:
        data.remove(['new'])
    for x in data:
        num += 1
        if svm.predict(x) == attack:
            total_a += 1
        elif svm.predict(x) == normal:
            total_n += 1
        else:
            print("OOPS")
            return    
    nratio = (float(total_n)/float(num))
    cur_scores.insert(len(cur_scores),nratio)
    print(str(cur_scores))
    aratio = (float(total_a)/float(num))    
    if nratio > 0.9:
        ret_[0] = '0'
        ret_[1] = cur_scores
        return ret_ 
    else:
        ret_[0] = '1'
        ret_[1] = cur_scores 
        return ret_


##################################################
######Removes the instances of new for fitting####
##################################################
##################################################

def removeNew(t_array):
    a_return = t_array
    for place in a_return:
        if place == ['new']:
            a_return.remove(['new'])    
    if ['new'] in a_return:
        print("WHOOPS!")
        return 1 
    return a_return


##################################################
#########Percentage validation####################
###########of the validation data#################
##################################################

def validateClass(svm,validation_array,f_index,new_cur):
    ret_ = dict()
    validate = 0.0
    num = 0.0
    print("length: " + str(len(validation_array)))
    for data in validation_array:
        num += 1
        cal_ = calClass(svm,data,cur_scores,new_cur)
        if cal_[0]  == format_array[f_index]:
            validate += 1
        
        print("NUM: " + str(int(num)) + " CLASSIFIED AS: " + str(cal_[0]))
    
    new_cur = 1 
    ret_[0] = float((validate)/(num))
    ret_[1] = cal_[1]
    return ret_

##################################################
################Main##############################
##################################################
##################################################

print("Creating the training data...")

##################################################
#############Create the attack and################
#################normal data and combine them#####
##################################################

instance_a0 = makeFitInstance(file_a0)
instance_a1 = makeFitInstance(file_a1)
instance_a2 = makeFitInstance(file_a2)
instance_a3 = makeFitInstance(file_a3)
instance_a4 = makeFitInstance(file_a4)
instance_a5 = makeFitInstance(file_a5)
instance_a6 = makeFitInstance(file_a6)
instance_a7 = makeFitInstance(file_a7)
instance_a8 = makeFitInstance(file_a8)
instance_a9 = makeFitInstance(file_a9)

instance_n0 = makeFitInstance(file_n0)
instance_n1 = makeFitInstance(file_n1)
instance_n2 = makeFitInstance(file_n2)
instance_n3 = makeFitInstance(file_n3)
instance_n4 = makeFitInstance(file_n4)
instance_n5 = makeFitInstance(file_n5)
instance_n6 = makeFitInstance(file_n6)
instance_n7 = makeFitInstance(file_n7)
instance_n8 = makeFitInstance(file_n8)
instance_n9 = makeFitInstance(file_n9)


clf = svm.SVC()
print("Starting cross validation with 10 folds...")

###Fold 1
###

fit_data0 = instance_a0[0] + instance_a1[0] + instance_a2[0] + instance_a3[0] + instance_a4[0] + instance_a5[0] + instance_a6[0] + instance_a7[0] + instance_a8[0] + instance_n0[0] + instance_n1[0] + instance_n2[0] + instance_n3[0] + instance_n4[0] + instance_n5[0] + instance_n6[0] + instance_n7[0] + instance_n8[0]
fit_classes0 = instance_a0[1] + instance_a1[1] + instance_a2[1] + instance_a3[1] + instance_a4[1] + instance_a5[1] + instance_a6[1] + instance_a7[1] + instance_a8[1] + instance_n0[1] + instance_n1[1] + instance_n2[1] + instance_n3[1] + instance_n4[1] + instance_n5[1] + instance_n6[1] + instance_n7[1] + instance_n8[1]


vali0 = makeValidationInstance(file_a9,format_index) + makeValidationInstance(file_n9,format_index)

print("Fold 1....")
clf.fit(removeNew(fit_data0),removeNew(fit_classes0))
per0 = validateClass(clf,vali0,format_index,new_cur)
print("% correct: " + str(per0[0]))

scores_ = per0[1]
binary_array.extend(roc_config(file_a9,1))
binary_array.extend(roc_config(file_n9,0))

print("scores_: " + str(scores_))
print("bin_array: " + str(binary_array))
fpr, tpr, thresholds = metrics.roc_curve(binary_array,scores_)
#plt.figure()
#plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc[2])
#plt.plot([0, 1], [0, 1], 'k--')
#plt.xlim([0.0, 1.0])
#plt.ylim([0.0, 1.05])
#plt.xlabel('False Positive Rate')
#plt.ylabel('True Positive Rate')
#plt.title('Receiver operating characteristic example')
#plt.legend(loc="lower right")
#plt.show()

###Fold 2
###

fit_data1 = instance_a1[0] + instance_a2[0] + instance_a3[0] + instance_a4[0] + instance_a5[0] + instance_a6[0] + instance_a7[0] + instance_a8[0] + instance_a9[0] + instance_n1[0] + instance_n2[0] + instance_n3[0] + instance_n4[0] + instance_n5[0] + instance_n6[0] + instance_n7[0] + instance_n8[0] + instance_n9[0]
fit_classes1 = instance_a1[1] + instance_a2[1] + instance_a3[1] + instance_a4[1] + instance_a5[1] + instance_a6[1] + instance_a7[1] + instance_a8[1] + instance_a9[1] + instance_n1[1] + instance_n2[1] + instance_n3[1] + instance_n4[1] + instance_n5[1] + instance_n6[1] + instance_n7[1] + instance_n8[1] + instance_n9[1]


vali1 = makeValidationInstance(file_a0,format_index) + makeValidationInstance(file_n0, format_index)

print("Fold 2...")
clf.fit(removeNew(fit_data1),removeNew(fit_classes1))
per1 = validateClass(clf,vali1,format_index,new_cur)
print("% correct: " + str(per1[0]))

scores_ = list()
scores_ = per1[1]
binary_array = list()
binary_array.extend(roc_config(file_a0,1))
binary_array.extend(roc_config(file_n0,0))

print("scores_: " + str(scores_))
print("bin_array: " + str(binary_array))
fpr, tpr, thresholds = metrics.roc_curve(binary_array,scores_)
###Fold 3
###

fit_data0 = instance_a2[0] + instance_a3[0] + instance_a4[0] + instance_a5[0] + instance_a6[0] + instance_a7[0] + instance_a8[0] + instance_a9[0] + instance_a0[0] + instance_n2[0] + instance_n3[0] + instance_n4[0] + instance_n5[0] + instance_n6[0] + instance_n7[0] + instance_n8[0] + instance_n9[0] + instance_n0[0]
fit_classes0 = instance_a2[1] + instance_a3[1] + instance_a4[1] + instance_a5[1] + instance_a6[1] + instance_a7[1] + instance_a8[1] + instance_a9[1] + instance_a0[1] + instance_n2[1] + instance_n3[1] + instance_n4[1] + instance_n5[1] + instance_n6[1] + instance_n7[1] + instance_n8[1] + instance_n9[1] + instance_n0[1]

vali2 = makeValidationInstance(file_a1,format_index) + makeValidationInstance(file_n1,format_index)

print("Fold 3...")
clf.fit(removeNew(fit_data0),removeNew(fit_classes0))
per2 = validateClass(clf,vali2,format_index,new_cur)
print("% correct: " + str(per2))

scores_ = list()
scores_ = per2[1]
binary_array = list()
binary_array.extend(roc_config(file_a1,1))
binary_array.extend(roc_config(file_n1,0))

print("scores_: " + str(scores_))
print("bin_array: " + str(binary_array))
fpr, tpr, thresholds = metrics.roc_curve(binary_array,scores_)


###Fold 4
###

fit_data0 = instance_a3[0] + instance_a4[0] + instance_a5[0] + instance_a6[0] + instance_a7[0] + instance_a8[0] + instance_a9[0] + instance_a0[0] + instance_a1[0] + instance_n3[0] + instance_n4[0] + instance_n5[0] + instance_n6[0] + instance_n7[0] + instance_n8[0] + instance_n9[0] + instance_n0[0] + instance_n1[0]
fit_classes0 = instance_a3[1] + instance_a4[1] + instance_a5[1] + instance_a6[1] + instance_a7[1] + instance_a8[1] + instance_a9[1] + instance_a0[1] + instance_a1[1] + instance_n3[1] + instance_n4[1] + instance_n5[1] + instance_n6[1] + instance_n7[1] + instance_n8[1] + instance_n9[1] + instance_n0[1] + instance_n1[1]

vali3 = makeValidationInstance(file_a2,format_index) + makeValidationInstance(file_n2,format_index)

print("Fold 4...")
clf.fit(removeNew(fit_data0),removeNew(fit_classes0))
per3 = validateClass(clf,vali3,format_index,new_cur)
print("% correct: " + str(per3))

scores_ = list()
scores_ = per3[1]
binary_array = list()
binary_array.extend(roc_config(file_a2,1))
binary_array.extend(roc_config(file_n2,0))

print("scores_: " + str(scores_))
print("bin_array: " + str(binary_array))
fpr, tpr, thresholds = metrics.roc_curve(binary_array,scores_)

###Fold 5
###

fit_data0 = instance_a4[0] + instance_a5[0] + instance_a6[0] + instance_a7[0] + instance_a8[0] + instance_a9[0] + instance_a0[0] + instance_a1[0] + instance_a2[0] + instance_n4[0] + instance_n5[0] + instance_n6[0] + instance_n7[0] + instance_n8[0] + instance_n9[0] + instance_n0[0] + instance_n1[0] + instance_n2[0]
fit_classes0 = instance_a4[1] + instance_a5[1] + instance_a6[1] + instance_a7[1] + instance_a8[1] + instance_a9[1] + instance_a0[1] + instance_a1[1] + instance_a2[1] + instance_n4[1] + instance_n5[1] + instance_n6[1] + instance_n7[1] + instance_n8[1] + instance_n9[1] + instance_n0[1] + instance_n1[1] + instance_n2[1]


vali4 = makeValidationInstance(file_a3,format_index) + makeValidationInstance(file_n3,format_index)

print("Fold 5...")
clf.fit(removeNew(fit_data0),removeNew(fit_classes0))
per4 = validateClass(clf,vali4,format_index,new_cur)
print("% correct: " + str(per4))

scores_ = list()
scores_ = per4[1]
binary_array = list()
binary_array.extend(roc_config(file_a3,1))
binary_array.extend(roc_config(file_n3,0))

print("scores_: " + str(scores_))
print("bin_array: " + str(binary_array))
fpr, tpr, thresholds = metrics.roc_curve(binary_array,scores_)
###Fold 6
###

fit_data0 = instance_a5[0] + instance_a6[0] + instance_a7[0] + instance_a8[0] + instance_a9[0] + instance_a0[0] + instance_a1[0] + instance_a2[0] + instance_a3[0] + instance_n5[0] + instance_n6[0] + instance_n7[0] + instance_n8[0] + instance_n9[0] + instance_n0[0] + instance_n1[0] + instance_n2[0] + instance_n3[0]
fit_classes0 = instance_a5[1] + instance_a6[1] + instance_a7[1] + instance_a8[1] + instance_a9[1] + instance_a0[1] + instance_a1[1] + instance_a2[1] + instance_a3[1] + instance_n5[1] + instance_n6[1] + instance_n7[1] + instance_n8[1] + instance_n9[1] + instance_n0[1] + instance_n1[1] + instance_n2[1] + instance_n3[1]

vali5 = makeValidationInstance(file_a4,format_index) + makeValidationInstance(file_n4,format_index)

print("Fold 6...")
clf.fit(removeNew(fit_data0),removeNew(fit_classes0))
per5 = validateClass(clf,vali5,format_index,new_cur)
print("% correct: " + str(per5))

scores_ = list()
scores_ = per5[1]
binary_array = list()
binary_array.extend(roc_config(file_a4,1))
binary_array.extend(roc_config(file_n4,0))

print("scores_: " + str(scores_))
print("bin_array: " + str(binary_array))
fpr, tpr, thresholds = metrics.roc_curve(binary_array,scores_)
###Fold 7
###

fit_data0 = instance_a6[0] + instance_a7[0] + instance_a8[0] + instance_a9[0] + instance_a0[0] + instance_a1[0] + instance_a2[0] + instance_a3[0] + instance_a4[0] + instance_n6[0] + instance_n7[0] + instance_n8[0] + instance_n9[0] + instance_n0[0] + instance_n1[0] + instance_n2[0] + instance_n3[0] + instance_n4[0]
fit_classes0 = instance_a6[1] + instance_a7[1] + instance_a8[1] + instance_a9[1] + instance_a0[1] + instance_a1[1] + instance_a2[1] + instance_a3[1] + instance_a4[1] + instance_n6[1] + instance_n7[1] + instance_n8[1] + instance_n9[1] + instance_n0[1] + instance_n1[1] + instance_n2[1] + instance_n3[1] + instance_n4[1]

vali6 = makeValidationInstance(file_a5,format_index) + makeValidationInstance(file_n5,format_index)

print("Fold 7...")
clf.fit(removeNew(fit_data0),removeNew(fit_classes0))
per6 = validateClass(clf,vali6,format_index,new_cur)
print("% correct: " + str(per6))

scores_ = list()
scores_ = per6[1]
binary_array = list()
binary_array.extend(roc_config(file_a5,1))
binary_array.extend(roc_config(file_n5,1))

print("scores_: " + str(scores_))
print("bin_array: " + str(binary_array))
fpr, tpr, thresholds = metrics.roc_curve(binary_array,scores_)
###Fold 8
###

fit_data0 = instance_a7[0] + instance_a8[0] + instance_a9[0] + instance_a0[0] + instance_a1[0] + instance_a2[0] + instance_a3[0] + instance_a4[0] + instance_a5[0] + instance_n7[0] + instance_n8[0] + instance_n9[0] + instance_n0[0] + instance_n1[0] + instance_n2[0] + instance_n3[0] + instance_n4[0] + instance_n5[0]
fit_classes0 = instance_a7[1] + instance_a8[1] + instance_a9[1] + instance_a0[1] + instance_a1[1] + instance_a2[1] + instance_a3[1] + instance_a4[1] + instance_a5[1] + instance_n7[1] + instance_n8[1] + instance_n9[1] + instance_n0[1] + instance_n1[1] + instance_n2[1] + instance_n3[1] + instance_n4[1] + instance_n5[1]

vali7 = makeValidationInstance(file_a6,format_index) + makeValidationInstance(file_n6,format_index)

print("Fold 8...")
clf.fit(removeNew(fit_data0),removeNew(fit_classes0))
per7 = validateClass(clf,vali7,format_index,new_cur)
print("% correct: " + str(per7))

scores_ = list()
scores_ = per7[1]
binary_array = list()
binary_array.extend(roc_config(file_a6,1))
binary_array.extend(roc_config(file_n6,0))

print("scores_: " + str(scores_))
print("bin_array: " + str(binary_array))
fpr, tpr, thresholds = metrics.roc_curve(binary_array,scores_)
###Fold 9
###

fit_data0 = instance_a8[0] + instance_a9[0] + instance_a0[0] + instance_a1[0] + instance_a2[0] + instance_a3[0] + instance_a4[0] + instance_a5[0] + instance_a6[0] + instance_n8[0] + instance_n9[0] + instance_n0[0] + instance_n1[0] + instance_n2[0] + instance_n3[0] + instance_n4[0] + instance_n5[0] + instance_n6[0]
fit_classes0 = instance_a8[1] + instance_a9[1] + instance_a0[1] + instance_a1[1] + instance_a2[1] + instance_a3[1] + instance_a4[1] + instance_a5[1] + instance_a6[1] + instance_n8[1] + instance_n9[1] + instance_n0[1] + instance_n1[1] + instance_n2[1] + instance_n3[1] + instance_n4[1] + instance_n5[1] + instance_n6[1]

vali8 = makeValidationInstance(file_a7,format_index) + makeValidationInstance(file_n7,format_index)

print("Fold 9...")
clf.fit(removeNew(fit_data0),removeNew(fit_classes0))
per8 = validateClass(clf,vali8,format_index,new_cur)
print("% correct: " + str(per8))

scores_ = list()
scores_ = per8[1]
binary_array = list()
binary_array.extend(roc_config(file_a7,1))
binary_array.extend(roc_config(file_n7,0))

print("scores_: " + str(scores_))
print("bin_array: " + str(binary_array))
fpr, tpr, thresholds = metrics.roc_curve(binary_array,scores_)
###Fold 10
####

fit_data0 = instance_a9[0] + instance_a0[0] + instance_a1[0] + instance_a2[0] + instance_a3[0] + instance_a4[0] + instance_a5[0] + instance_a6[0] + instance_a7[0] + instance_n9[0] + instance_n0[0] + instance_n1[0] + instance_n2[0] + instance_n3[0] + instance_n4[0] + instance_n5[0] + instance_n6[0] + instance_n7[0]
fit_classes0 = instance_a9[1] + instance_a0[1] + instance_a1[1] + instance_a2[1] + instance_a3[1] + instance_a4[1] + instance_a5[1] + instance_a6[1] + instance_a7[1] + instance_n9[1] + instance_n0[1] + instance_n1[1] + instance_n2[1] + instance_n3[1] + instance_n4[1] + instance_n5[1] + instance_n6[1] + instance_n7[1]

vali9 = makeValidationInstance(file_a8,format_index) + makeValidationInstance(file_n8,format_index)

print("Fold 10...")
clf.fit(removeNew(fit_data0),removeNew(fit_classes0))
per9 = validateClass(clf,vali9,format_index,new_cur)
print("% correct: " + str(per9))

scores_ = list()
scores_ = per9[1]
binary_array = list()
binary_array.extend(roc_config(file_a8,1))
binary_array.extend(roc_config(file_n8,0))

print("scores_: " + str(scores_))
print("bin_array: " + str(binary_array))
fpr, tpr, thresholds = metrics.roc_curve(binary_array,scores_)

total_percent = per0[0] + per1[0] + per2[0] + per3[0] + per4[0] + per5[0] + per6[0] + per7[0] + per8[0] + per9[0]
print("Total cross validation percentage: " + str(float((total_percent)/(float(10.0))))) 



