class PatternRelationship < ActiveRecord::Base
  belongs_to :source, :class_name => 'Pattern'
  belongs_to :target, :class_name => 'Pattern'
  belongs_to :relationship_type

  validates :source, :target, :relationship_type, :presence => true
end
