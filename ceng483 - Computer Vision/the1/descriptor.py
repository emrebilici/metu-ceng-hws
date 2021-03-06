import argparse

parser = argparse.ArgumentParser()
add_arg = parser.add_argument

add_arg('--input', default='dataset/', type=str,
        help='Directory of images.')
add_arg('--output', default=None, type=str,
        help='Prefix of the file to output descriptors.')
add_arg('--dense', default=0, type=int,
        help='Dense SIFT or not.')
add_arg('--step', default=5, type=int,
        help='If dense, then specify step size.')
add_arg('--train', default=1, type=int,
        help='Training mode (1) or te sklearn.cluster import MiniBatchKMeans
        kmeans = MiniBatchKMeans(n_clusters=N_CLUSTERS, max_iter=MAX_ITERS,
                batch_size=BTC_SIZE).fit(descriptorsArray)

    if JUST_MSE:
        #print(kmeans.inertia_ / len(descriptorsArray))
        print(kmeans.inertia_)
        exit()

    print('KMeans is done. Load descriptor dictionaries.')

    descriptors = None

    with open(INPUT_PRE + '_train_descDict', 'rb') as fp:
       descriptors = pickle.load(fp) 

    print('Done. Construct each image\'s histogram.')

    labels = kmeans.labels_

    del kmeans

    it = 0

    for descriptorDict in descriptors:

        descriptorDict['histogram'] = np.zeros(shape=(N_CLUSTERS,))
        ndescriptors = len(descriptorDict['descriptors'])

        for cid in labels[it: it+ndescriptors]:

            descriptorDict['histogram'][cid] += 1

        np.divide(descriptorDict['histogram'], ndescriptors)

        del descriptorDict['descriptors']
        
        it += ndescriptors
    
    print('Done. Save dictionaries with labels and log work.')

    with open(OUTPUT_PRE + '_train_labeledDict', 'wb') as fp:
       pickle.dump(descriptors, fp)

    with open(OUTPUT_PRE + '_train_clusters.log', "w") as fp:
        fp.write("K=" + str(N_CLUSTERS) + '\n')
        fp.write("MaxIters=" + str(MAX_ITERS) + '\n')
        if BTC_SIZE != 0:
            fp.write("BatchSize=" + str(BTC_SIZE) + '\n')
        else:
            fp.write("BatchSize=None\n")

    print('Done.')

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           