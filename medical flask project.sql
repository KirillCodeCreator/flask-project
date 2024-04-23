CREATE TABLE `user` (
  `id` int PRIMARY KEY,
  `specialization_id` int,
  `firstname` varchar(255),
  `lastname` varchar(255),
  `middlename` varchar(255),
  `email` varchar(255),
  `hashed_password` varchar(255),
  `birthday` date,
  `phone` varchar(255),
  `polis` varchar(255),
  `role` varchar(255),
  `location` varchar(255),
  `modified_date` datatime
);

CREATE TABLE `specialization` (
  `id` int PRIMARY KEY,
  `title` time
);

CREATE TABLE `timeinterval` (
  `id` int PRIMARY KEY,
  `starttime` time,
  `endtime` time
);

CREATE TABLE `appointment` (
  `id` int PRIMARY KEY,
  `doctor_id` int,
  `date` date,
  `timeinterval_id` int,
  `modified_date` datetime
);

CREATE TABLE `appointmentpatient` (
  `id` int PRIMARY KEY,
  `appointment_id` int,
  `patient_id` int,
  `result` varchar(255),
  `modified_date` datetime
);

ALTER TABLE `user` ADD FOREIGN KEY (`specialization_id`) REFERENCES `specialization` (`id`);

ALTER TABLE `appointment` ADD FOREIGN KEY (`timeinterval_id`) REFERENCES `timeinterval` (`id`);

ALTER TABLE `appointment` ADD FOREIGN KEY (`doctor_id`) REFERENCES `user` (`id`);

ALTER TABLE `appointmentpatient` ADD FOREIGN KEY (`appointment_id`) REFERENCES `appointment` (`id`);

ALTER TABLE `appointmentpatient` ADD FOREIGN KEY (`patient_id`) REFERENCES `user` (`id`);
