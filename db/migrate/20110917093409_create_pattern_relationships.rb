class CreatePatternRelationships < ActiveRecord::Migration
  def change
    create_table :pattern_relationships do |t|
      t.integer :source_id
      t.integer :target_id
      t.integer :relationship_type_id
      t.text :description

      t.timestamps
    end
  end
end
