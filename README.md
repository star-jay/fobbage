
# fobbage
The ultimate quiz

# creating a new model
- pick an app where you want the model to belong 

>  /fobbage/quizes/
- create a new class in the models.py file, inheriting from the models.Model class. 
>     class  Quiz(models.Model):
- add fields to the model
>     title = models.CharField(max_length=255)
- add string representation or other functions
>     def  __str__(self):  
>         """ string representation """ 	 
>         return  "Quiz: {}".format(self.quiz)
- create a new factory for your model in `tests/factories/<app>_factories.py`
>     class  QuizFactory(factory.Factory):
>         """ Factory that creates an example quiz """
>         class  Meta:
>               model = Quiz
>               
>         # add a value for the required fields
>         title =  "factory quiz"
- create a unit test where you test your first method
> 
>     @pytest.mark.django_db
>     def  test_quiz_string_representation():
>         """Make a clear string representation for the quiz"""
>         quiz = QuizFactory()
>         assert quiz.__str__() ==  'Quiz: '  +  str(quiz.title)

