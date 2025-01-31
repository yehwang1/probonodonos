PRAGMA foreign_keys = ON;

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('heisenberg', 'Walter White', 'heisenberg@jpwynn.edu',
        'heisenberg.jpg',
        'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'
);

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('itssaulgoodman', 'Saul Goodman', 'saulgoodman@yahoo.edu',
        'saulgoodman.jpg',
        'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'
);

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('capncook', 'Jesse Pinkman', 'capncook@jpwynne.edu',
        'capncook.jpg',
        'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'
);

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('hector', 'Hector Salamanca', 'hector@cartel.edu',
        'hector.jpg',
        'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'
);

INSERT INTO posts(postid, filename, owner)
VALUES (
    1, '122a7d27ca1d7420a1072f695d9290fad4501a41.jpg', 'heisenberg'
);

INSERT INTO posts(postid, filename, owner)
VALUES (
    2, 'ad7790405c539894d25ab8dcf0b79eed3341e109.jpg', 'saulgoodman'
);

INSERT INTO posts(postid, filename, owner)
VALUES (
    3, '9887e06812ef434d291e4936417d125cd594b38a.jpg', 'heisenberg'
);

INSERT INTO posts(postid, filename, owner)
VALUES (
    4, '2ec7cf8ae158b3b1f40065abfb33e81143707842.jpg', 'hector'
);

INSERT INTO likes(owner, postid)
VALUES (
    'heisenberg', 1
);

INSERT INTO likes(owner, postid)
VALUES (
    'capncook', 1
);

INSERT INTO likes(owner, postid)
VALUES (
    'saulgoodman', 1
);

INSERT INTO likes(owner, postid)
VALUES (
    'heisenberg', 2
);

INSERT INTO likes(owner, postid)
VALUES (
    'capncook', 2
);

INSERT INTO likes(owner, postid)
VALUES (
    'heisenberg', 3
);

INSERT INTO following(username1, username2)
VALUES (
    'heisenberg', 'saulgoodman'
);

INSERT INTO following(username1, username2)
VALUES (
    'heisenberg', 'capncook'
);

INSERT INTO following(username1, username2)
VALUES (
    'saulgoodman', 'heisenberg'
);

INSERT INTO following(username1, username2)
VALUES (
    'saulgoodman', 'capncook'
);

INSERT INTO following(username1, username2)
VALUES (
    'capncook', 'heisenberg'
);

INSERT INTO following(username1, username2)
VALUES (
    'capncook', 'hector'
);

INSERT INTO following(username1, username2)
VALUES (
    'hector', 'capncook'
);

INSERT INTO comments(commentid, owner, postid, text)
VALUES (
    1, 'heisenberg', 3, 'this looks amazing!'
);

INSERT INTO comments(commentid, owner, postid, text)
VALUES (
    2, 'saulgoodman', 3, 'is there any chance you are around the abq area?'
);

INSERT INTO comments(commentid, owner, postid, text)
VALUES (
    3, 'capncook', 3, 'love the clothing'
);

INSERT INTO comments(commentid, owner, postid, text)
VALUES (
    4, 'heisenberg', 2, 'dapper'
);

INSERT INTO comments(commentid, owner, postid, text)
VALUES (
    5, 'saulgoodman', 1, 'better call saul!'
);

INSERT INTO comments(commentid, owner, postid, text)
VALUES (
    6, 'heisenberg', 1, 'i am the one who knocks'
);

INSERT INTO comments(commentid, owner, postid, text)
VALUES (
    7, 'hector', 4, 'ding'
);