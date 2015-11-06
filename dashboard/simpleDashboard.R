library(rmongodb)

mongo <- mongo.create()

acts <- mongo.find.all(mongo, 
                       "runkeeper.activities", 
                       '{"type": "Running", 
                         "duration": {"$gt": 0}}',
                       data.frame = TRUE)
acts$month <- substr(acts$start_time, 1, 7)
acts$pace <- acts$duration / 60 / acts$total_distance

stats_by_months <- aggregate(x = acts[, c("pace")], by = list(month = acts$month), FUN = "mean")
stats_by_months
# plot(stats_by_months$month, stats_by_months$x)
plot(stats_by_months$x)
axis(1, labels = stats_by_months$month)
