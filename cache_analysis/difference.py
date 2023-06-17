from datetime import datetime
import matplotlib.pyplot as plt


def count_events_in_interval(bins, times, interval):
    # starting from end to incorporate reverse chronological order
    for i in range(-1, -len(times), -1):
        latest_status_time = datetime.fromtimestamp(float(times[i]))
        previous_status_time = datetime.fromtimestamp(float(times[i - 1]))
        diff = (latest_status_time - previous_status_time).total_seconds()
        minutes, seconds = divmod(diff, 60)
        # if the difference in minutes between reception of two serial status is less than current TTL interval
        # increase the count in that interval or else the other one.
        if minutes <= interval:
            bins[f"<={interval}"] += 1
        else:
            bins[f">{interval}"] += 1


def create_data(file_name, interval, data_points, cache_hits):
    # we receive a lot of status count the difference between status and bin it as per interval.
    total_status_count = 0
    intervals = {f"<={interval}": 0, f">{interval}": 0}
    with open(file_name, 'r') as f:
        for line in f.readlines():
            line = line.strip('\n')

            fr, status_timestamps = line.split(',')[0], line.split(',')[1]
            status_timestamps = status_timestamps.split(' ')
            # if we have received multiple statuses
            if len(status_timestamps) > 1:
                total_status_count += len(status_timestamps) - 1
                count_events_in_interval(intervals, status_timestamps, interval)
        data_points.append(intervals)
        cache_hit_percentage = intervals[f"<={interval}"] / total_status_count
        text = f"Cache Hit = {cache_hit_percentage * 100:.2f}%"
        cache_hits.append(text)


def plot_histogram(file):
    bins = {"<=30": 0, "31-60": 0, "61-90": 0, "91-120": 0, ">120": 0}
    total_status = 0
    with open(file, 'r') as f:
        for line in f.readlines():
            line = line.strip('\n')
            fr, times = line.split(',')[0], line.split(',')[1]
            times = times.split(' ')
            total_status += len(times) - 1
            for i in range(-1, -len(times), -1):
                t1 = datetime.fromtimestamp(float(times[i]))
                t2 = datetime.fromtimestamp(float(times[i - 1]))
                diff = (t1 - t2).total_seconds()
                minutes, seconds = divmod(diff, 60)
                if minutes <= 30:
                    bins["<=30"] += 1
                elif minutes <= 60:
                    bins["31-60"] += 1
                elif minutes <= 90:
                    bins["61-90"] += 1
                elif minutes <= 120:
                    bins["91-120"] += 1
                else:
                    bins[">120"] += 1
        # print(bins)
        cache_hit = bins["<=30"] / total_status
        text = "Cache Hit = {:.2f}%".format(cache_hit * 100)
        print(total_status)
        print(text)
        plt.bar(*zip(*bins.items()))
        plt.text(0.15, 0.9, bins, transform=plt.gcf().transFigure)
        plt.text(0.6, 1112.9, text)
        plt.text(4.0, 4000, total_status)
        plt.title(file, y=-0.15)
        name = 'histogram.png'
        plt.savefig(name)


def plot_within_interval(data, text, file, intervals):
    fig, ax = plt.subplots(len(data), 1)
    fig.tight_layout()
    fig.subplots_adjust(hspace=1.0)

    for i in range(len(data)):
        ax[i].bar(*zip(*data[i].items()))
        ax[i].set_title(str(intervals[i]) + ' - ' + text[i])
        ax[i].plot()

    plt.savefig('all_intervals_{}.png'.format(file[:file.find('.')]))


def main_interval():
    # interval in minutes
    intervals = [30, 60, 120, 180, 1440, 2880]
    for file in ['query.csv']:
        data_points = list()
        cache_hits = list()
        for interval in intervals:
            create_data(file, interval, data_points, cache_hits)
        print(data_points)
        print(cache_hits)
        plot_within_interval(data_points, cache_hits, file, intervals)


# main_interval()

plot_histogram('query.csv')
