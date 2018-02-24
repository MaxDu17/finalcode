import tensorflow as tf
import numpy as np
import random
import os
from make_sets import Setmaker as SM
class Hyperparameters:
    INPUT_LAYER = 43
    HIDDEN_LAYER = 100 #Modify??
    OUTPUT_LAYER = 3
    NUM_EPOCHS = 5000
    BATCH_NUMBER = 240
    LEARNING_RATE = 0.1

class Information:
    INPUT_DIMENSIONS = 43
    INPUT_TIME_DIV = 0.125
    INPUT_SECTORS = 8
    SAMPLE_RATE = 4096



set_maker = SM()
HYP = Hyperparameters()

W_In = tf.Variable(tf.random_normal(shape = [HYP.INPUT_LAYER,HYP.HIDDEN_LAYER], stddev = 0.1 ))#note: this used to have a mean of zero, so check that
W_Hidd =tf.Variable(tf.random_normal(shape = [HYP.HIDDEN_LAYER,HYP.HIDDEN_LAYER], stddev = 0.1 ))
W_Out =tf.Variable(tf.random_normal(shape = [HYP.HIDDEN_LAYER,HYP.OUTPUT_LAYER], stddev = 0.1 ))

B_In = tf.Variable(tf.zeros(HYP.HIDDEN_LAYER))
B_Hidd = tf.Variable(tf.zeros(HYP.HIDDEN_LAYER))
B_Out = tf.Variable(tf.zeros(HYP.OUTPUT_LAYER))

with tf.name_scope("placeholders"):
    X = tf.placeholder(shape=[1,HYP.INPUT_LAYER],name = "input",dtype = tf.float32)
    Y = tf.placeholder(shape=[1,HYP.OUTPUT_LAYER],name = "one_hot_labels",dtype = tf.int8)
    last_hidd = tf.placeholder(shape=[1,HYP.HIDDEN_LAYER],name = "previous_hidden_layer", dtype = tf.float32)
with tf.device("/device:GPU:0"):
    with tf.name_scope("input_propagation"):
        hidd_layer = tf.matmul(X,W_In)
        hidd_layer = tf.add(hidd_layer,B_In)

    with tf.name_scope("hidden_propagation"):
        propagated_prev_hidd_layer = tf.matmul(last_hidd,W_Hidd)
        propagated_prev_hidd_layer = tf.add(propagated_prev_hidd_layer,B_Hidd)
        concat_hidd_layer = tf.add(hidd_layer,propagated_prev_hidd_layer)
        concat_hidd_layer = tf.sigmoid(concat_hidd_layer)
        next_hidd_layer = concat_hidd_layer
    with tf.name_scope("logit_output"):
        output_logit = tf.matmul(concat_hidd_layer,W_Out)
        output_logit = tf.add(output_logit, B_Out)
    with tf.name_scope("prediction_and_loss"):
        output_prediction = tf.nn.softmax(output_logit)
        loss = tf.nn.softmax_cross_entropy_with_logits(logits = output_logit,labels=Y,name = "sparse_softmax_loss_function")
        total_loss = tf.reduce_mean(loss)
    with tf.name_scope("train"):
        optimizer = tf.train.AdagradOptimizer(learning_rate=HYP.LEARNING_RATE).minimize(total_loss)

with tf.name_scope("summaries_and_saver"):
    tf.summary.histogram("W_Hidd", W_Hidd)
    tf.summary.histogram("W_In", W_In)
    tf.summary.histogram("W_Out", W_Out)

    tf.summary.histogram("B_Hidd", B_Hidd)
    tf.summary.histogram("B_In", B_In)
    tf.summary.histogram("B_Out", B_Out)

    tf.summary.scalar("Loss",total_loss)

    summary_op = tf.summary.merge_all()
    saver = tf.train.Saver()
with tf.Session() as sess:
    ckpt = tf.train.get_checkpoint_state(os.path.dirname('GRAPHCHECKPOINTS/checkpoint'))
    if ckpt and ckpt.model_checkpoint_path:
        saver.restore(sess, ckpt.model_checkpoint_path)
    sess.run(tf.global_variables_initializer())
    writer = tf.summary.FileWriter("GRAPHS/",sess.graph)
    set_maker.get_test_set()
    total_loss_ = 0
    for epoch in range(HYP.NUM_EPOCHS):
        set_maker.load_next_epoch()

        for batch_number in range(HYP.BATCH_NUMBER):
            input_array,label = set_maker.load_next_train_sample(batch_number = batch_number)
            one_hot_label = set_maker.one_hot_from_label(label=label)
            one_hot_label = np.reshape(one_hot_label,[1,3])
            counter = 0
            first = True
            for slice in input_array:
                slice = np.reshape(slice,[1,43])

                if counter == 15:

                    next_hidd_layer_,output_logit_,output_prediction_,loss_,total_loss_,summary,_ = sess.run([next_hidd_layer,
                                                                                    output_logit,
                                                                                    output_prediction,
                                                                                    loss,
                                                                                    total_loss,
                                                                                    summary_op,
                                                                                    optimizer], feed_dict=
                    {
                        X: slice,
                        Y: one_hot_label,
                        last_hidd: prev_hidd_layer_
                    })
                else:
                    if(first):
                        prev_hidd_layer_ = np.zeros(shape = HYP.HIDDEN_LAYER)
                        prev_hidd_layer_ = np.reshape(prev_hidd_layer_,[1,100])
                        first = False

                    next_hidd_layer_ = sess.run(next_hidd_layer,feed_dict =
                    {
                        X: slice,
                        last_hidd: prev_hidd_layer_
                    })
                    prev_hidd_layer_ = next_hidd_layer_
                    counter+= 1
        print("end epoch")
        writer.add_summary(summary,global_step=epoch)
        if epoch%500 ==0:
            saver.save(sess, "GRAPHCHECKPOINTS/rough_run",global_step = epoch)
            print(total_loss_)
    writer.close()