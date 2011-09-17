# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rake db:seed (or created alongside the db with db:setup).
#
# Examples:
#
#   cities = City.create([{ :name => 'Chicago' }, { :name => 'Copenhagen' }])
#   Mayor.create(:name => 'Emanuel', :city => cities.first)
RelationshipType.delete_all

RelationshipType.create(:name => 'Variant')
RelationshipType.create(:name => 'Extension')
RelationshipType.create(:name => 'Base')

Pattern.delete_all

Pattern.create(:name => 'Model-view-controller pattern',
               :slug => 'mvc-pattern',
               :description => 'The pattern isolates "domain logic"
                               (the application logic for the user) from the
                               user interface (input and presentation),
                               permitting independent development,
                               testing and maintenance of each (separation
                               of concerns).')

Pattern.create(:name => 'Layers pattern',
               :slug => 'layers-pattern',
               :description => 'A layer is a group of reusable components that
                                are reusable in similar circumstances.')

Pattern.create(:name => 'Proxy pattern',
               :slug => 'proxy-pattern',
               :description => 'A proxy, in its most general form, is a class
                                functioning as an interface to something else.
                                The proxy could interface to anything: a network
                                connection, a large object in memory, a file, or
                                some other resource that is expensive or
                                impossible to duplicate.')

Pattern.create(:name => 'Strategy pattern',
               :slug => 'strategy-pattern',
               :description => 'The strategy pattern defines a family of
                                algorithms, encapsulates each one, and makes
                                them interchangeable. Strategy lets the
                                algorithm vary independently from clients that
                                use it.')

Pattern.create(:name => 'Template method pattern',
               :slug => 'template-method-pattern',
               :description => 'A template method defines the program skeleton
                                of an algorithm. One or more of the algorithm
                                steps can be overridden by subclasses to allow
                                differing behaviors while ensuring that the
                                overarching algorithm is still followed.')

Pattern.create(:name => 'Facade pattern',
               :slug => 'facade-pattern',
               :description => 'A facade is an object that provides a simplified
                                interface to a larger body of code, such as a
                                class library.')