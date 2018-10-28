from __future__ import print_function
import tensorflow as tf
import numpy as np
import time
import h5py

label_train = np.load("train_labels.npy").astype(np.float32)
label_test = np.load("test_labels.npy").astype(np.float32)
h5_train = h5py.File('train_words.h5','r')
doc_train = h5_train['d1'][:]
h5_test = h5py.File('test_words.h5','r')
doc_test = h5_test['d2'][:]
print("data_loaded")


print (doc_train.shape)
print (label_train.shape)


# Parameters
lr = 0.005
training_epochs = 100
batch_size = 2048
display_step = 1

# tf Graph Input
x = tf.placeholder(tf.float32, [None, doc_train.shape[1]]) 
y = tf.placeholder(tf.float32, [None, 50]) 
# Set model weights
W = tf.Variable(tf.random_normal([doc_train.shape[1], 50]))
b = tf.Variable(tf.random_normal([50]))

weight=tf.reshape(tf.reduce_sum(y,0)/tf.reduce_sum(tf.reduce_sum(y,0)),[1,50])

# Construct model
pred = (tf.matmul(x, W) + b) # Softmax
weight_per_label = tf.transpose( tf.matmul(y, tf.transpose(weight)) ) 

xent = tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y)
loss = tf.reduce_mean(xent) #shape 1
regularizer = tf.nn.l2_loss(W)
cost = tf.reduce_mean(loss + 0.01 * regularizer)
# Gradient Descent
optimizer = tf.train.AdamOptimizer(lr).minimize(cost)

prediction = tf.nn.softmax(tf.matmul(x, W) + b)
#train_prediction = tf.nn.softmax(tf.matmul(doc_train, W) + b)
def accuracy(predictions, labels):
    p=0
    k=predictions.shape[0]
    for i in range(predictions.shape[0]):
        if (labels[i,np.argmax(predictions[i,:])]!=0):
            p=p+1
    return (100.0 * p/ labels.shape[0])
# Initialize the variables (i.e. assign their default value)
init = tf.global_variables_initializer()
save_cost_acc_lr = np.zeros((training_epochs,3))
#save_accuracy = np.zeros((training_epochs,1))
# Start training
with tf.Session() as sess:

    # Run the initializer
    sess.run(init)
    begin_time = time.time()
    # Training cycle
    for epoch in range(training_epochs):
        avg_cost = 0.
        total_batch = int(doc_train.shape[0]/batch_size)
        # Loop over all batches
        for i in range(total_batch):
            batch_xs=doc_train[i*batch_size:i*batch_size+batch_size,:]
            batch_ys = label_train[i*batch_size:i*batch_size+batch_size,:]
            _, c = sess.run([optimizer, cost], feed_dict={x: batch_xs,
                                                          y: batch_ys})
            # Compute average loss
            avg_cost += c / total_batch
            accuracy_epoch = accuracy(sess.run(prediction, feed_dict={x: doc_test}),label_test)
        # Display logs per epoch step
        if (epoch+1) % display_step == 0:
            print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(avg_cost))
        print (accuracy(sess.run(prediction, feed_dict={x: doc_test}),label_test))
        save_cost_acc_lr[epoch,0] = avg_cost
        save_cost_acc_lr[epoch,1] = accuracy_epoch
        save_cost_acc_lr[epoch,2] = lr
        #save_accuracy[epoch,0] = accuracy_epoch

    print("Optimization Finished!")
    print("Total Time: %3.2fs" % float(time.time() - begin_time))
    print ("train_accuracy=",accuracy(sess.run(prediction, feed_dict={x: doc_train}),label_train))
    print ("test_accuracy=",accuracy(sess.run(prediction, feed_dict={x: doc_test}),label_test))
    np.save("lr_const_cost_acc_lr",save_cost_acc_lr)
