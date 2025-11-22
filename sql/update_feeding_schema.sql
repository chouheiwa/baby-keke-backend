-- Add duration_left and duration_right columns to feeding_records table
ALTER TABLE feeding_records ADD COLUMN duration_left INT COMMENT '左侧时长(秒)';
ALTER TABLE feeding_records ADD COLUMN duration_right INT COMMENT '右侧时长(秒)';
