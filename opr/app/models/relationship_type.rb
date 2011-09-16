class RelationshipType < ActiveRecord::Base
  default_scope :order => 'title'
  has_many :pattern_relationships
  validates :title, :presence => true, :uniqueness => {:case_sensitive => false}
end
