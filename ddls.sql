create table user
(
    id            int auto_increment primary key,
    name          varchar(100)                         not null,
    email         varchar(100) unique                  not null,
    password      varchar(100)                         not null,
    last_login    datetime                             null,
    reset_token   varchar(50)                          null,
    token_created datetime                             null,
    IS_ACTIVE     tinyint(1) default 1                 not null,
    provider      varchar(255)                         not null,
    provider_id   varchar(255)                         null,
    principal_id  varchar(255)                         null,
    create_at     datetime   default CURRENT_TIMESTAMP not null
);

# create table user_permission
# (
#     user_id    int          not null,
#     permission varchar(100) not null,
#     primary key (user_id, permission),
#     constraint user_role_ibfk_1
#         foreign key (user_id) references user (id)
# );

create table configuration_metadata
(
    id                 int auto_increment primary key,
    batch_id           varchar(36)                        not null comment 'UUID given to a set of updates done together as part of a single configuration',
    configuration_name varchar(100)                       not null comment 'Example: "Google - Siteclick Postback"',
    service_name       varchar(50)                        not null,
    table_name         varchar(100)                       not null,
    row_id             int                                not null comment 'id of the affected remote database row',
    sql_query          text                               not null comment 'sql query used to make the update',
    user_id            int                                not null,
    timestamp          datetime default CURRENT_TIMESTAMP not null,
    constraint configuration_metadata_ibfk_1
        foreign key (user_id) references user (id)
);

create table configuration_google_external_product
(
    id                                      bigint auto_increment primary key ,
    account_id                              varchar(255) not null,
    campaign_id                             varchar(255) not null,
    external_partner_product_naming_enabled tinyint(1)   not null,
    unique account_id__campaign_id (account_id, campaign_id)
);

create table configuration_google_siteclick_postback
(
    id                                      bigint auto_increment primary key ,
    mcc_id                                  varchar(255) not null,
    account_id                              varchar(255) not null,
    campaign_id                             varchar(255) not null,
    rollout_type                            varchar(255) not null,
    active                                  tinyint(1)   not null,
    unique account_id__campaign_id (account_id, campaign_id)
);

create table configuration_google_parallel_predictions
(
    id                                      bigint auto_increment primary key,
    account_id                              varchar(255) not null,
    partner_id                              varchar(255) not null,
    deal_type                               varchar(255) not null,
    active                                  tinyint(1)   not null,
    unique account_id__partner_id__deal_type (account_id, partner_id, deal_type)
);

create table configuration_google_postback_with_commission
(
    id                                      bigint auto_increment primary key,
    mcc_id                                  varchar(255) not null,
    account_id                              varchar(255) not null,
    campaign_id                             varchar(255) not null,
    from_date                               datetime     not null,
    to_date                                 datetime             ,
    active                                  tinyint(1)   not null,
    unique account_id__campaign_id (account_id, campaign_id)
);


insert into user (name, email, password, IS_ACTIVE, provider) value ('yaniv1', 'yaniv1@gmail.com', 'yaniv1', 1, 'okta');

INSERT INTO configuration_google_external_product (account_id, campaign_id, external_partner_product_naming_enabled) VALUES ('1617543791', '16135915876', 0);
INSERT INTO configuration_google_external_product (account_id, campaign_id, external_partner_product_naming_enabled) VALUES ('1617543791', '2026992924', 1);
INSERT INTO configuration_google_external_product (account_id, campaign_id, external_partner_product_naming_enabled) VALUES ('1617543791', '2029722674', 1);
INSERT INTO configuration_google_external_product (account_id, campaign_id, external_partner_product_naming_enabled) VALUES ('3986547011', '16218935452', 1);
INSERT INTO configuration_google_external_product (account_id, campaign_id, external_partner_product_naming_enabled) VALUES ('3986547011', '16218935455', 1);
INSERT INTO configuration_google_external_product (account_id, campaign_id, external_partner_product_naming_enabled) VALUES ('6114238072', '17188399821', 0);
INSERT INTO configuration_google_external_product (account_id, campaign_id, external_partner_product_naming_enabled) VALUES ('3257315645', '58893849494', 1);