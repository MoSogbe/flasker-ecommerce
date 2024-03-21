from market import app
from flask_sqlalchemy import SQLAlchemy

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ogydvexzweaqfq:d01ebfe8d607b6e2f40e802d7826598e0573f858f7b694772790c00edb14670e@ec2-52-54-200-216.compute-1.amazonaws.com:5432/d5ge7ve4iqdsd6'
app.config['SECRET_KEY'] = '540a114d5672840527eb71aa'
db = SQLAlchemy(app)
if __name__ == '__main__':
    
    app.run(debug=True)