import numpy as np
from tqdm import tqdm
import os
from os.path import dirname, join

project_root = dirname(dirname(__file__))
data_path = join(project_root, 'Data', '')


class PrimeFrog:
    def __init__(self):
        self.target = 'PPPPNNPPPNPPNPN'
        self.n = len(self.target)

    def findAllPath(self, Path, lengthRemain):
        if lengthRemain == 0:
            yield Path
        else:
            curLocation = Path[-1]
            if curLocation == 1:
                yield from self.findAllPath(Path + [2], lengthRemain - 1)
                yield from self.findAllPath(Path + [2], lengthRemain - 1)  # repeat to obey probability law
            elif curLocation == 500:
                yield from self.findAllPath(Path + [499], lengthRemain - 1)
                yield from self.findAllPath(Path + [499], lengthRemain - 1)  # repeat to obey probability law
            else:
                yield from self.findAllPath(Path + [curLocation - 1], lengthRemain - 1)
                yield from self.findAllPath(Path + [curLocation + 1], lengthRemain - 1)

    def PrimeQ(self, n):
        """
        Assumes that n is a positive natural number
        """
        # We know 1 is not a prime number
        if n == 1:
            return False

        i = 2
        # This will loop from 2 to int(sqrt(x))
        while i * i <= n:
            # Check if i divides x without leaving a remainder
            if n % i == 0:
                # This means that n has a factor in between 2 and sqrt(n)
                # So it is not a prime number
                return False
            i += 1
        # If we did not find any factor in the above loop,
        # then n is a prime number
        return True

    def computeProbability(self, Path):
        num2str = ''.join(map(lambda x: 'P' if self.PrimeQ(x) else 'N', Path))
        assert len(num2str) == len(self.target), 'Illegal matach'
        prob = [2 / 3 if num2str[ix] == self.target[ix] else 1 / 3 for ix in range(len(num2str))]
        probability = np.prod(prob)
        booleanMatch = [num2str[ix] == self.target[ix] for ix in range(len(num2str))]
        numerator = 2 ** booleanMatch.count(True)
        denominator = 3 ** len(self.target)
        assert abs(probability - numerator / denominator) < 1e-4

        return probability, numerator, denominator

    def main(self):

        running_prob, total_den, total_num = 0, 0, 0
        # with open(data_path + 'p329.txt', 'w') as f:
        for loc in tqdm(range(1, 501)):

            for path in self.findAllPath([loc], self.n - 1):
                probability, numerator, denominator = self.computeProbability(path)
                running_prob += probability
                total_den = denominator
                total_num += numerator


                    # num2str = ''.join(map(lambda x: 'P' if self.PrimeQ(x) else 'N', path))
                    # f.write("%s\n" % num2str)
        running_prob /= (500* 2 ** (self.n-1))
        total_den = total_den * (500* 2 ** (self.n-1))
        assert abs(running_prob - total_num / total_den) < 1e-4, f'{running_prob} = {total_num}/ {total_den}'
        return running_prob, total_num, total_den


if __name__ == '__main__':
    frog = PrimeFrog()

    print(frog.main())

    # (6.796996401016548e-06, 798961412, 117546246144000)