import dejavu.decoder as decoder
import fingerprint
import multiprocessing
import os
import pickle


class Dejavu(object):
    def __init__(self, config):
        super(Dejavu, self).__init__()

        self.config = config

        self.limit = None

    def fingerprint_directory(self, path, extensions, nprocesses=None):

        try:
            nprocesses = nprocesses or multiprocessing.cpu_count()
        except NotImplementedError:
            nprocesses = 1
        else:
            nprocesses = 1 if nprocesses <= 0 else nprocesses

        pool = multiprocessing.Pool(nprocesses)

        filenames_to_fingerprint = []
        for filename, _ in decoder.find_files(path, extensions):


            if decoder.path_to_songname(filename) in self.songnames_set:
                continue

            filenames_to_fingerprint.append(filename)


        worker_input = zip(filenames_to_fingerprint,
                           [self.limit] * len(filenames_to_fingerprint))


        iterator = pool.imap_unordered(_fingerprint_worker,
                                       worker_input)


        while True:
            try:
                song_name, hashes = iterator.next()
            except multiprocessing.TimeoutError:
                continue
            except StopIteration:
                break
            except:
                print("Failed fp")

                import traceback, sys
                traceback.print_exc(file=sys.stdout)
            else:
		print "Already FP"

        pool.close()
        pool.join()

    def fp_file(self, filepath, song_name=None):
    	
        ssong_name, hashes = _fingerprint_worker(filepath,
                                                self.limit,
                                                song_name=song_name)

        # finger print to send
        song_name = filepath
        f = open(song_name + '.txt', 'wb')
        pickle.dump(hashes, f)
        f.close()

def _fingerprint_worker(filename, limit=None, song_name=None):
    try:
        filename, limit = filename
    except ValueError:
        pass

    songname, extension = os.path.splitext(os.path.basename(filename))

    song_name = song_name or songname

    channels, Fs = decoder.read(filename, limit)

    result = set()

    channel_amount = len(channels)
    for channeln, channel in enumerate(channels):
        hashes = fingerprint.fingerprint(channel, Fs=Fs)

        result |= set(hashes)

    return song_name, result


def chunkify(lst, n):
    return [lst[i::n] for i in xrange(n)]
