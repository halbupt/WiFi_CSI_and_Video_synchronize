import math


def split(train_d, label_t, scene, person, flag, objflag):
    x = []
    y = []
    x_l = []
    y_l = []

    if flag == 1:
        # find the number of samples for each action
        num_sample = len(train_d)
        # split by propotion: training & testing data split as 7: 3
        num_train = math.floor(num_sample * 0.7)  # set the split number of train sample for each action

        if objflag == 'SVM':
            x = train_d[1:num_train][:][:][:][:]  # train_d: [num * 30 * 3 * 3 * 200]
            x_l = train_d[num_train + 1:None][:][:][:][:]

        elif objflag == 'csinet':
            x = train_d[1:num_train][:][:][:]  # train_d: [num * 30 * 1 * 1]
            x_l = train_d[num_train + 1:None][:][:][:]

        y = label_t[1:num_train]
        y_l = label_t[num_train + 1:None]

    elif flag == 2:  # person 1 train, person 3 test
        num_p = person
        if num_p == 1:  # person 1-->train
            x = train_d
            y = label_t
        else:
            x_l = train_d
            y_l = label_t


    elif flag == 2.5:  # person 3 train, person 1 test
        num_p = person
        if num_p == 3:  # person 3-->train
            x = train_d
            y = label_t
        else:
            x_l = train_d
            y_l = label_t


    elif flag == 3:  # scene 1&2 train, scene 3 test
        num_s = scene
        if num_s == 1 or num_s == 2:  # scene 1 & 2 -->train
            x = train_d
            y = label_t
        else:
            x_l = train_d
            y_l = label_t

    train_data = x  # [num * 270 * 200]
    train_label = y
    test_data = x_l
    test_label = y_l

    return train_data, train_label, test_data, test_label
