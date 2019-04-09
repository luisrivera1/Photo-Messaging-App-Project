create table Login(lid serial primary key, uusername varchar(20), upassword varchar(20));

create table Users(uid serial primary key, ufirstname varchar(20), ulastname varchar(20), uemail varchar(50), uusername varchar(20), upassword varchar(20));

create table Validates(login_id integer references Login(lid), user_id integer references Users(uid), primary key(login_id, user_id));

create table Contacts(owner_id integer references Users(uid), contact_id integer references Users(uid), primary key(owner_id, contact_id)); 

create table Chat(cid serial primary key, cname varchar(20), cadmin integer references Users(uid)); 

create table isMember(user_id integer references Users(uid), chat_id integer references Chat(cid), primary key(user_id, chat_id)); 

create table Post(pid serial primary key, puser integer references Users(uid), pphoto varchar(100), pmessage varchar(100), pdate DATE);

create table isReply(reply_id integer references Post(pid), original_id integer references Post(pid), primary key(reply_id, original_id));  

create table Has(chat_id integer references Chat(cid), post_id integer references Post(pid), primary key(chat_id, post_id)); 

create table Reaction(rid serial primary key, rDate DATE, type varchar(10), usr integer references Users(uid),  post integer references Post(pid)); 

create table Hashtag(hid serial primary key, htext varchar(30)); 

create  table Tagged(post_id integer references Post(pid), hashtag_id integer references Hashtag(hid), primary key(post_id, hashtag_id));
