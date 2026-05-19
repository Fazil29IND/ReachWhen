create database ReachWhen;
use ReachWhen;
create table PredictionData(
    TrainNo INT NOT NULL,
    PickUpStation VARCHAR(200) NOT NULL,
    DropStation VARCHAR(200) NOT NULL,
    Distance INT NOT NULL,
    NumberOfStops INT NOT NULL,
    ArrivalTime TIME NOT NULL,
    DestinationTime TIME NOT NULL,
    ActualDuration INT NOT NULL,
    PredictedDuration INT NOT NULL );
select * from PredictionData;