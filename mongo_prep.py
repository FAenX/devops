from string import Template
import argparse
import subprocess
import sys

super_user = Template('''
        db.createUser(
            {
                user: '$USER', 
                pwd: '$PASSWORD', 
                 roles: [
                       
                        { role: 'userAdminAnyDatabase', db: 'admin' } 
                    ]
            });
    ''')

app_user = Template('''
        db.createUser(
            {
                user: '$USER', 
                pwd: '$PASSWORD', 
                roles:[{ role: 'readWrite', db: '$DATABASE' }]
            });
    ''')

# terminal argument parser
def parseArgs():
    # create a parser
    parser = argparse.ArgumentParser(description='App options.')
    parser.add_argument("user", help="mongo user")
    parser.add_argument("--dbname", help="name of collection")
    parser.add_argument("--admin", action='store_true' ,help="mongo user")
    
    return parser.parse_args()

if __name__ == '__main__':
    args = parseArgs()
    # print(args)
    user = args.user
    admin = args.admin
    dbname = 'test'
    if args.dbname:
        dbname = args.dbname

    MONGO_PASSWORD='T72askY8Am3Yt3Q2'
    m1 = '"{}" '.format(super_user.safe_substitute(
        USER=user, PASSWORD=MONGO_PASSWORD, 
        ))

    if admin == False:     
        
        m1 = '"{}"'.format(app_user.safe_substitute(
            USER=user, PASSWORD=MONGO_PASSWORD, DATABASE=dbname))
    
    m1 = 'mongo {} --eval {}'.format(dbname, m1)
    print(m1)


    c1 = subprocess.Popen(m1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    c1.wait()
    if c1.returncode == 0:
        print('created user')       
    else:       
        print(c1.stdout.read())
        print(c1.returncode)
        sys.exit('creating user')

