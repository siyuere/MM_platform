CREATE TABLE task_tab (
    id BIGINT PRIMARY KEY,
    task_name VARCHAR(255),
    input_path VARCHAR(255),
    output_path VARCHAR(255),
    status SMALLINT
);

CREATE TABLE model_task_result_tab (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
		task_id BIGINT NOT NULL, #FK
    model_id BIGINT NOT NULL,
    task_status SMALLINT NOT NULL,
    creat_time BIGINT NOT NULL,
    finish_time BIGINT NOT NULL,
    accuracy VARCHAR(255) NOT NULL
);

CREATE TABLE model_tab (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
		path TEXT NOT NULL,
    creat_time BIGINT NOT NULL,
    model_name VARCHAR(255) NOT NULL
);

CREATE TABLE prediction_result_tab (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
		path TEXT NOT NULL,
    model_name VARCHAR(255) NOT NULL,
    structure VARCHAR(255) NOT NULL,
    result VARCHAR(255) NOT NULL
);
