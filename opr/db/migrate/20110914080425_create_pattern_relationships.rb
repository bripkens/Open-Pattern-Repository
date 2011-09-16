class CreatePatternRelationships < ActiveRecord::Migration
  def self.up
    create_table :pattern_relationships do |t|
      t.integer :source_id
      t.integer :target_id
      t.integer :relationship_type_id
      t.text :description

      t.timestamps
    end
  end

  def self.down
    drop_table :pattern_relationships
  end
end
