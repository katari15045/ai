import tensorflow as tf

tf_y = tf.placeholder(tf.float32, shape=[None, 2])
tf_lyr_out = tf.placeholder(tf.float32, shape=[None, 2])
tf_acc, tf_temp = tf.metrics.accuracy(labels=tf.argmax(tf_y, axis=1), predictions=tf.argmax(tf_lyr_out, axis=1), name="tf_acc")


sess = tf.Session()
sess.run(tf.global_variables_initializer())
sess.run(tf.local_variables_initializer())

# vars_to_init = tf.get_collection(tf.GraphKeys.LOCAL_VARIABLES, scope="tf_acc")
# vars_initializer = tf.variables_initializer(var_list=vars_to_init)
# sess.run(vars_initializer)

a = sess.run([tf_temp], feed_dict={tf_y:[[1, 0], [0, 1], [1, 0]], tf_lyr_out:[[1, 0], [1, 0], [1, 0]]})
c = sess.run([tf_acc], feed_dict={tf_y:[[1, 0], [0, 1], [1, 0]], tf_lyr_out:[[1, 0], [1, 0], [1, 0]]})
print("acc-a: {0}, acc-b: {1}, acc-c: {2}".format(a, a, c))

